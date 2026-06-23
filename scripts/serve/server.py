"""Loopback-only intake HTTP server (ADR-0013-T1 skeleton + ADR-0013-T4 upload route).

`build_server(port)` constructs a stdlib `http.server.ThreadingHTTPServer` bound to
`("127.0.0.1", port)` ONLY — never `0.0.0.0`/`""`/a routable interface (ADR-0013
Confirmation 1: the first network surface the system opens, off-machine-unreachable
by construction). The bind literal lives in exactly one place (`_LOOPBACK`) so the
downstream tasks extend the handler without re-specifying the bind.

The handler serves GET `/` with the existing intake wizard — the body IS
`generate.run('intake')`'s rendered HTML (the server adds a transport, not a new
wizard); a non-`/` GET returns 404. POST `/upload` (ADR-0013-T4) is a thin chain:
stage the multipart body (`multipart.stage_uploads`, ADR-0013-T2) -> route the
staged file into the UNCHANGED `ingest.run`/`dna.land` seam (`route.route_upload`)
-> re-render the wizard via `generate.run('intake')` reflecting the new load-state.
The server serves NO generated artifact live — intake-only (ADR-0013 Falsification 3;
the route table is exactly {GET `/`, POST `/upload`}). Stopping is `srv.shutdown()` +
`srv.server_close()`, the clean operator-stop path.
"""

import xml.etree.ElementTree as ET
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from scripts.serve.multipart import MAX_UPLOAD_BYTES, UploadTooLarge

# The single loopback-bind site. Changing this away from 127.0.0.1 breaks the
# ADR-0013-T1 criterion-1 structural assertion + the off-machine-unreachable
# guarantee — non-negotiable (ADR-0013 Falsification 1).
_LOOPBACK = "127.0.0.1"

# The default operator port for `python -m scripts.serve` (OQ-2 fail-loud names it).
DEFAULT_PORT = 8765

# The whole-request byte ceiling, rejected on Content-Length BEFORE the body is read
# (HTTP 413) so a giant body never materializes in RAM. It sits a multipart-overhead
# margin above the per-file ceiling so a real Apple-Health export (the file at the
# per-file ceiling, plus boundary/header framing) still fits.
_MULTIPART_OVERHEAD_MARGIN = 8 * 1024 * 1024
MAX_REQUEST_BYTES = MAX_UPLOAD_BYTES + _MULTIPART_OVERHEAD_MARGIN


class _BoundedReader:
    """A read-bounded view over `rfile` that never yields more than `length` bytes.

    `read(n)` reads in chunks but stops at the Content-Length so the multipart
    parser sees a body capped at the declared length — `self.rfile.read(length)`
    materialized the whole body in RAM (defeating multipart's mid-stream ceiling);
    this hands the parser a stream instead, so `multipart._stage_file`'s per-file
    ceiling bounds memory.

    Attributes:
        stream (BinaryIO): The underlying request rfile.
        remaining (int): Bytes still permitted before the declared length is hit.
    """

    def __init__(self, stream, length):
        self.stream = stream
        self.remaining = length

    def read(self, size=-1):
        """Read up to `size` bytes, never crossing the declared Content-Length."""
        if self.remaining <= 0:
            return b""
        want = self.remaining if size is None or size < 0 else min(size, self.remaining)
        data = self.stream.read(want)
        self.remaining -= len(data)
        return data


def _render_intake(*, store_root=None, dna_root=None):
    """Return the intake wizard HTML — the GET `/` body and the POST re-render body.

    Drives `generate.run('intake')` (which RE-READS the live store + dropzone
    load-state, so a re-render after an upload reflects the just-landed readings/files)
    and reads the produced file's text. The server is glue: the body is exactly the
    rendered wizard. `store_root`/`dna_root` are the test-seam roots the POST handler
    ingested into; None falls through to `generate.run`'s production defaults.
    """
    from scripts.generate.generate import run as generate_run

    return generate_run("intake", _root=store_root, _dna_root=dna_root).read_text()


class IntakeRequestHandler(BaseHTTPRequestHandler):
    """Serve the intake wizard at GET `/`; stage->route->re-render at POST `/upload`.

    GET `/` writes HTTP 200 + the `generate.run('intake')` body; any other GET 404s.
    POST `/upload` stages the multipart body, routes the staged file into the unchanged
    `ingest.run`/`dna.land` seam, and re-renders the wizard reflecting the new
    load-state. Any other POST 404s — the route table is intake-only {GET `/`, POST
    `/upload`}, never a directory listing or an artifact-serving route.

    Attributes:
        store_root: The time-series store root the POST handler ingests into and
            re-renders from (None -> the production `vault/store/` default).
        dna_root: The DNA dropzone the POST handler lands DNA into and re-renders from
            (None -> the production `vault/dna/raw/` default).
        scaffold_root: The gitignored operator-record root the POST handler's
            form-field capture writes record-only values into (None -> the production
            `vault/scaffold/filled/` default).
        identity_config: The instance operator-identity token config the POST handler's
            form-field capture threads into `persist_capture` so operator-identity PII
            detection is non-empty (None -> `pii_scan`'s `vault/meta/operator-identity.txt`
            default). The H-2 wiring (ADR-0017-T1): every capture call site threads this
            through the same class-attr seam as `store_root`/`scaffold_root`, so dropping
            it never silently disables identity detection.
        client: The model client the POST `/chat` per-turn dispatch makes its ONE outbound
            model call through (ADR-0016-T1; None -> a default `ModelClient` on the no-train
            lane). The only model egress is via `scripts/model/`; the `/chat` route makes no
            outbound call of its own (the single-egress-class boundary).
    """

    store_root = None
    dna_root = None
    scaffold_root = None
    identity_config = None
    client = None

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        self._write_html(200, _render_intake(store_root=self.store_root, dna_root=self.dna_root))

    def do_POST(self):
        if self.path == "/chat":
            self._do_chat()
            return
        if self.path != "/upload":
            self.send_error(404)
            return
        import tempfile

        from scripts.serve import capture, route
        from scripts.serve.multipart import stage_uploads

        # Reject an over-ceiling Content-Length BEFORE reading the body so a giant
        # upload never materializes in RAM (HTTP 413, not a dropped connection).
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            # A non-numeric Content-Length raised here, OUTSIDE the old guarded block,
            # killing the request thread. Re-render the wizard rather than drop.
            self._write_html(400, _render_intake(store_root=self.store_root, dna_root=self.dna_root))
            return
        if length > MAX_REQUEST_BYTES:
            self._413_too_large()
            return

        store_root = self.store_root
        dna_root = self.dna_root
        scaffold_root = self.scaffold_root
        identity_config = self.identity_config
        step = None
        try:
            # A length-bounded reader streams the body to the multipart parser, so
            # multipart's mid-stream per-file ceiling bounds memory (the prior
            # `rfile.read(length)` read the whole body into RAM, defeating it).
            with tempfile.TemporaryDirectory() as staging:
                staged = stage_uploads(
                    self.headers.get("Content-Type"), _BoundedReader(self.rfile, length), staging
                )
                for file_part in staged["files"]:
                    route.route_upload(file_part["path"], root=store_root, dna_root=dna_root)
                # The form-field capture (ADR-0014-T1): route each submitted field by its
                # data class — a wired de-identified token to the store via the unchanged
                # store.append, a record-only/raw value to the gitignored scaffold. The
                # `step` field (a control field, not captured) selects the Step-6 handoff
                # re-render; capture.persist_capture ignores it as a non-wired record field
                # — strip it so it never lands as a stray scaffold value.
                fields = dict(staged["fields"])
                step = fields.pop("step", None)
                if fields:
                    # Thread the instance identity_config (H-2, ADR-0017-T1): without it
                    # the free-text PII scan's operator-identity detection is empty —
                    # the factory-to-component wiring gap this closes.
                    capture.persist_capture(
                        fields, root=store_root, scaffold_root=scaffold_root,
                        identity_config=identity_config,
                    )
        except (SystemExit, ValueError, zipfile.BadZipFile, ET.ParseError):
            # A real operator input must NOT kill the request thread. SystemExit: an
            # ambiguous/unknown extension (`_detect_source`). ValueError: a fail-loud
            # land rejection (`dna.land`/the adapter) or a malformed multipart body.
            # BadZipFile/ParseError: a corrupt `.zip`/`export.xml`. Re-render the wizard
            # so the operator can pick a source / re-upload, not a stack trace + drop.
            self._write_html(200, _render_intake(store_root=store_root, dna_root=dna_root))
            return
        except UploadTooLarge:
            # A part crossed multipart's per-file ceiling mid-stream — same 413 surface
            # as the up-front Content-Length reject (the body was bounded, not RAM-held).
            self._413_too_large()
            return

        # Re-render reflecting the new load-state (the store/dropzone were just written).
        # The re-render carries the wizard's Step-6 `/generate-plan` handoff state — the
        # server performs 0 in-app generation; Step 6 routes the operator to the agent path.
        self._write_html(200, _render_intake(store_root=store_root, dna_root=dna_root))

    def _413_too_large(self):
        """Write a 413 wizard re-render for an over-ceiling upload (no dropped connection)."""
        self._write_html(413, _render_intake(store_root=self.store_root, dna_root=self.dna_root))

    def _do_chat(self):
        """Run one POST `/chat` per-turn dispatch and write the JSON turn receipt.

        Reads a JSON turn body (`{"turn", "conversation"?, "covered_domains"?,
        "declined_domains"?}`), runs the `chat.dispatch_turn` chain over the instance roots
        + the injected model client (the ONE outbound model call is the dispatch's
        `client.converse` — the route makes no outbound call of its own), and writes the
        per-turn receipt (assistant reply + capture receipt + progress) as JSON. A malformed
        body or a dispatch/model-client exception is CAUGHT and answered with a degraded
        response — the request thread is never dropped (mirroring `/upload`'s catch-and-
        re-render thread-survival posture). The dispatch's own fail-closed degraded turn (a
        failed model call) is returned verbatim — no fabricated reply/fact, no store write.
        """
        import json

        from scripts.model.client import ModelClient
        from scripts.serve import chat

        # The injected instance client (tests inject a mock backend); None falls through to
        # a default `ModelClient` on the no-train lane. The SDK import is lazy inside the
        # backend, so resolving the client here adds no outbound client to the serve layer.
        client = self.client if self.client is not None else ModelClient()

        try:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            body = json.loads(raw.decode("utf-8")) if raw else {}
            turn_text = body.get("turn", "")
            conversation = body.get("conversation", [])
            covered = body.get("covered_domains", [])
            declined = body.get("declined_domains", [])
            receipt = chat.dispatch_turn(
                turn_text, conversation, covered, declined, client=client,
                store_root=self.store_root, scaffold_root=self.scaffold_root,
                identity_config=self.identity_config,
            )
        except Exception:
            # Thread survival (AC-6): a malformed body / a dispatch exception must NOT kill
            # the request thread. Answer with a degraded response, never a dropped
            # connection — and never a fabricated reply/fact or a store write. The shape
            # mirrors `chat._degraded_turn` (carries `reason`) so the two degraded surfaces
            # cannot silently diverge.
            self._write_json(400, {
                "reply": None, "receipt": {"store": [], "scaffold": [], "dropped": []},
                "progress": None, "degraded": True, "degrade_to": "form",
                "reason": "bad request",
            })
            return
        self._write_json(200, receipt)

    def _write_json(self, status, obj):
        """Write a JSON response body (the `/chat` turn-receipt response-write site)."""
        import json

        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _write_html(self, status, html):
        """Write an HTTP response with the HTML body (the single response-write site)."""
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        """Silence the default per-request stderr access log."""


def build_server(port, *, store_root=None, dna_root=None, scaffold_root=None,
                 identity_config=None, client=None):
    """Construct the loopback-bound intake server on `port`.

    The POST `/upload` handler ingests file uploads into `store_root`/`dna_root`,
    captures form fields by data class (wired tokens -> `store_root`, record-only
    values -> `scaffold_root`), and re-renders the wizard from the store. All four
    default to None, which falls through to the production `vault/store/` /
    `vault/dna/raw/` / `vault/scaffold/filled/` / `vault/meta/operator-identity.txt`
    defaults (so the operator entry `python -m scripts.serve` serves the real instance).
    Tests bind tmp roots so the E2E never touches the real store/dropzone/scaffold.

    Args:
        port (int): The TCP port to bind on loopback; 0 picks an ephemeral port.
        store_root (str | Path, optional): The store root the POST handler ingests into.
        dna_root (str | Path, optional): The DNA dropzone the POST handler lands into.
        scaffold_root (str | Path, optional): The gitignored operator-record root the
            form-field capture writes record-only values into.
        identity_config (str | Path, optional): The instance operator-identity token
            config the form-field capture threads into `persist_capture` (the H-2 seam,
            ADR-0017-T1); None falls through to `pii_scan`'s default.
        client (optional): The model client the POST `/chat` dispatch makes its one outbound
            model call through (ADR-0016-T1); None -> a default `ModelClient`. Tests inject a
            mock backend so the E2E never makes a live API call.

    Returns:
        (ThreadingHTTPServer) A server bound to ("127.0.0.1", port). Stop it with
        `srv.shutdown()` + `srv.server_close()`.
    """
    handler = type("BoundIntakeRequestHandler", (IntakeRequestHandler,),
                   {"store_root": store_root, "dna_root": dna_root,
                    "scaffold_root": scaffold_root, "identity_config": identity_config,
                    "client": client})
    return ThreadingHTTPServer((_LOOPBACK, port), handler)
