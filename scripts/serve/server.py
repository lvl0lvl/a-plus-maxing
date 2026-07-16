"""Loopback-only intake HTTP server (ADR-0013-T1 skeleton + ADR-0013-T4 upload route).

`build_server(port)` constructs a stdlib `http.server.ThreadingHTTPServer` bound to
`("127.0.0.1", port)` ONLY — never `0.0.0.0`/`""`/a routable interface (ADR-0013
Confirmation 1: the first network surface the system opens, off-machine-unreachable
by construction). The bind literal lives in exactly one place (`_LOOPBACK`) so the
downstream tasks extend the handler without re-specifying the bind.

The handler serves GET `/` with the served app shell (ADR-0029-T1) — the body IS
`generate.run('app')`'s rendered HTML (the server adds a transport, not a new view);
a non-`/` GET returns 404. POST `/upload` (ADR-0013-T4) is a thin chain: stage the
multipart body (`multipart.stage_uploads`, ADR-0013-T2) -> route the staged file into
the UNCHANGED `ingest.run`/`dna.land` seam (`route.route_upload`) -> re-render the app
shell via `generate.run('app')` reflecting the new load-state. The server serves NO
generated dashboard/report artifact live (ADR-0013 Falsification 3); the route table
is {GET `/`, GET `/settings/key`, GET `/settings/trackers`, GET `/conversation`,
POST `/upload`, POST `/chat`, POST `/settings/key`, POST `/settings/tracker`,
POST `/care-chat`, POST `/confirm-extraction`, POST `/confirm-curation`,
POST `/confirm-plan-change`, POST `/generate-plan`, POST `/plan-loop`}. POST `/confirm-extraction`
(ADR-0030-T3) lands ONLY the operator-confirmed subset of an unrecognized-format
upload's extracted readings through the UNCHANGED sink — the `/upload` handler surfaces
those readings and lands 0. POST `/generate-plan` authors + records a plan for each
`plan_schema.PLAN_DOMAINS` over the stored data via the UNCHANGED
`scripts.plan.generate_plan` caller (the serve layer re-implements no assembly/safety
logic — it only CALLS it) and answers the re-rendered Plan zone + per-domain outcomes
as JSON. Stopping is `srv.shutdown()` +
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

# Loopback origin hosts — a request whose `Origin` is one of these came from the operator's own
# served app (same machine); any OTHER present Origin is a cross-site page (the CSRF vector).
_LOOPBACK_ORIGIN_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})


def _is_cross_site_origin(origin):
    """True when `origin` is present AND not a loopback origin — a browser cross-site request.

    A browser attaches the `Origin` header to every cross-origin POST, so a present non-loopback
    Origin is the CSRF vector. An ABSENT Origin (a non-browser client — curl / the CLI) or a
    LOOPBACK Origin (the operator's own served app on 127.0.0.1/localhost) is NOT cross-site and is
    allowed. Used to gate POST `/upload`, whose `multipart/form-data` content-type is itself a
    CORS-simple type, so the `application/json` 415 gate the other POST routes use cannot cover it.

    Args:
        origin (str | None): The request's `Origin` header value.

    Returns:
        (bool) True to refuse (a browser cross-site POST), False to allow.
    """
    if not origin:
        return False
    from urllib.parse import urlparse

    host = (urlparse(origin).hostname or "").lower()
    return host not in _LOOPBACK_ORIGIN_HOSTS

# The whole-request byte ceiling, rejected on Content-Length BEFORE the body is read
# (HTTP 413) so a giant body never materializes in RAM. It sits a multipart-overhead
# margin above the per-file ceiling so a real Apple-Health export (the file at the
# per-file ceiling, plus boundary/header framing) still fits.
_MULTIPART_OVERHEAD_MARGIN = 8 * 1024 * 1024
MAX_REQUEST_BYTES = MAX_UPLOAD_BYTES + _MULTIPART_OVERHEAD_MARGIN

# The whole-body ceiling for POST /settings/key. An API key is ~100 chars; 16 KiB is a
# generous margin that still rejects a giant body before it is read into RAM.
_SETTINGS_MAX_BYTES = 16 * 1024

# The whole-body ceiling for POST /confirm-extraction. The confirmed subset is a small JSON
# array of Line-Field-Set readings; 1 MiB is a generous margin for a full lab panel that
# still rejects a giant body on Content-Length BEFORE it is read into RAM (the same
# bounded-memory posture as _SETTINGS_MAX_BYTES, ADR-0030-T3 review SHOULD-FIX D).
_CONFIRM_MAX_BYTES = 1024 * 1024


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
    """Return the served app-shell HTML — the GET `/` body and the POST re-render body.

    Drives `generate.run('app')` (which RE-READS the live store + dropzone load-state,
    so a re-render after an upload reflects the just-landed readings/files in the app
    shell's Upload Documents cards) and reads the produced file's text. The server is
    glue: the body is exactly the rendered app shell. `store_root`/`dna_root` are the
    test-seam roots the POST handler ingested into; None falls through to
    `generate.run`'s production defaults. (The name is retained from the ADR-0013
    intake-wizard era for blast-radius minimization — every POST re-render site reuses it.)
    """
    from scripts.generate.generate import run as generate_run

    return generate_run("app", _root=store_root, _dna_root=dna_root).read_text()


class IntakeRequestHandler(BaseHTTPRequestHandler):
    """Serve the intake wizard at GET `/`; stage->route->re-render at POST `/upload`.

    GET `/` writes HTTP 200 + the `generate.run('app')` body; any other GET 404s.
    POST `/upload` stages the multipart body, routes the staged file into the unchanged
    `ingest.run`/`dna.land` seam, and re-renders the app shell reflecting the new
    load-state. Any other POST 404s — the route table is {GET `/`, GET `/settings/key`,
    GET `/settings/trackers`, GET `/conversation`, POST `/upload`, POST `/chat`,
    POST `/care-chat`, POST `/settings/key`, POST `/settings/tracker`,
    POST `/confirm-extraction`, POST `/confirm-curation`, POST `/confirm-plan-change`,
    POST `/generate-plan`, POST `/plan-loop`}, never a directory listing or an artifact-serving route.

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
    key_resolver = None
    key_store = None
    loop_dispatch = None
    loop_deid_client = None
    # The care-lane presentation client the POST /confirm-plan-change act fires the deferred
    # tailoring seam through (ADR-0040-T4). None at the un-wired production site keeps the seam a
    # pass-through (0 spend); the deferred OQ-5 confirm UX wires it through this class-attr seam,
    # mirroring `loop_dispatch`/`identity_config`.
    tailor_client = None

    def do_GET(self):
        # Match on the PATH only, ignoring any `?query`/`#fragment`. A query string must not 404 the
        # app: it is the operator's cache-bust escape hatch — `/?v=2` is a URL the browser has never
        # cached, so it is guaranteed a fresh fetch when a stale copy of `/` is stuck in cache.
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == "/settings/key":
            self._key_status()
            return
        if path == "/settings/trackers":
            self._tracker_status()
            return
        if path == "/conversation":
            self._do_get_conversation()
            return
        if path != "/":
            self.send_error(404)
            return
        self._write_html(200, _render_intake(store_root=self.store_root, dna_root=self.dna_root))

    def do_POST(self):
        if self.path == "/chat":
            self._do_chat()
            return
        if self.path == "/care-chat":
            self._do_care_chat()
            return
        if self.path == "/settings/key":
            self._save_key()
            return
        if self.path == "/settings/tracker":
            self._save_tracker_token()
            return
        if self.path == "/confirm-extraction":
            self._do_confirm_extraction()
            return
        if self.path == "/confirm-curation":
            self._do_confirm_curation()
            return
        if self.path == "/confirm-plan-change":
            self._do_confirm_plan_change()
            return
        if self.path == "/generate-plan":
            self._do_generate_plan()
            return
        if self.path == "/plan-loop":
            self._do_plan_loop()
            return
        if self.path != "/upload":
            self.send_error(404)
            return

        # CSRF gate (SEC / o2gj): /upload requires `multipart/form-data` — itself a CORS-simple
        # content-type — so the `application/json` 415 gate the other POST routes use CANNOT cover it.
        # A cross-site `fetch(url, {mode:"no-cors", body:<FormData>})` sends multipart with no
        # preflight, and an unrecognized-format file drives the metered `route.route_upload` ->
        # `client.extract_readings` spend on the operator's key. Refuse a browser cross-site request (a
        # present, non-loopback Origin) BEFORE any work — the same-origin served app and non-browser
        # (no-Origin) clients pass; a browser always sends Origin on a cross-origin POST.
        if _is_cross_site_origin(self.headers.get("Origin")):
            self._write_json(403, {"error": "cross-site origin refused"})
            return
        import tempfile

        from scripts.ingest.pdf_extract import PdfExtractError
        from scripts.model.client import ModelCallError
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
                extracted = []
                partial = False
                notes = []
                for file_part in staged["files"]:
                    # Thread the instance client into T2's discriminated router: a recognized
                    # format lands via the unchanged seam (returns a source str); an
                    # unrecognized format routes through the no-train extract lane (returns
                    # {"extracted_readings": [...]}) and lands 0 — those readings are surfaced
                    # for the operator-confirm step (POST /confirm-extraction), never
                    # auto-landed (ADR-0030 NFR-2). With self.client None the unrecognized
                    # path preserves today's SystemExit (re-rendered below); extraction
                    # activates only when a client is injected (the operator-gated live lane).
                    result = route.route_upload(
                        file_part["path"], client=self.client, root=store_root, dna_root=dna_root
                    )
                    if isinstance(result, dict):
                        extracted.extend(result["extracted_readings"])
                        # The honest-partial signal (ADR-0031-T4): the PDF arm reports
                        # extraction_complete / extraction_note; the non-PDF arm omits them
                        # (the absent key defaults to complete / no note). ANY incomplete file
                        # marks the whole upload partial; each truthy note is collected.
                        if not result.get("extraction_complete", True):
                            partial = True
                        note = result.get("extraction_note")
                        if note:
                            notes.append(note)
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
        except (SystemExit, ValueError, zipfile.BadZipFile, ET.ParseError, ModelCallError, PdfExtractError):
            # A real operator input must NOT kill the request thread. SystemExit: an
            # ambiguous/unknown extension (`_detect_source`) with no client to extract.
            # ValueError: a fail-loud land rejection (`dna.land`/the adapter) or a malformed
            # multipart body. BadZipFile/ParseError: a corrupt `.zip`/`export.xml`.
            # ModelCallError: a failed no-train extraction (`extract_readings` fail-closed,
            # ADR-0030-T3 forward-note). PdfExtractError: a total local PDF-extraction failure
            # (T1's fail-loud raise, ADR-0031-T4) — degrade like ModelCallError with 0 fabricated
            # readings. Re-render the app shell so the operator can pick a source / re-upload,
            # not a stack trace + drop.
            self._write_html(200, _render_intake(store_root=store_root, dna_root=dna_root))
            return
        except UploadTooLarge:
            # A part crossed multipart's per-file ceiling mid-stream — same 413 surface
            # as the up-front Content-Length reject (the body was bounded, not RAM-held).
            self._413_too_large()
            return

        # An unrecognized-format upload surfaced extracted readings OR an honest-partial signal
        # — answer with the JSON review payload (lands 0; POST /confirm-extraction is the ONLY
        # landing path, the confirm-gate). The payload key is `readings`, the SAME key
        # `/confirm-extraction` consumes, so the confirm UI re-posts the operator-confirmed
        # subset verbatim with no remap (review SHOULD-FIX E). F1 (ADR-0031-T4): the signal
        # surfaces even when `extracted == []` but `partial == True` — a too-dense / over-budget
        # PDF must NOT collapse into the silent "no new data" re-render. A truly-empty /
        # recognized-format / fields-only upload (extracted == [] AND not partial) still falls
        # through to the app-shell re-render below (the honest empty-vs-partial distinction).
        if extracted or partial:
            self._write_json(200, {"readings": extracted, "partial": partial, "notes": notes})
            return

        # ADR-0033-0035-T8: the final-save care-agent review. When this form-capture just
        # completed the profile (T6's predicate) AND a usable no-train key + client are present,
        # fire the review and deliver its clarifying questions + status in the response. With no
        # key / no client / an incomplete profile it returns None and the existing HTML re-render
        # below is the honest 0-spend degrade.
        review_response = self._maybe_care_review(store_root, scaffold_root, identity_config, fields)
        if review_response is not None:
            # Persist the care-review OPENING questions to the conversation vault so a later reload
            # restores the full conversation (the questions + the operator's replies), not only the
            # replies. A recording failure must not drop the response (the review already succeeded).
            try:
                from scripts.serve import conversation_store
                for question in (review_response.get("questions") or []):
                    if question:
                        conversation_store.record_turn("care", "assistant", question,
                                                       root=self._conversation_root())
            except Exception:
                pass
            self._write_json(200, review_response)
            return

        # Re-render reflecting the new load-state (the store/dropzone were just written).
        # The re-render carries the wizard's Step-6 `/generate-plan` handoff state — the
        # server performs 0 in-app generation; Step 6 routes the operator to the agent path.
        self._write_html(200, _render_intake(store_root=store_root, dna_root=dna_root))

    def _413_too_large(self):
        """Write a 413 wizard re-render for an over-ceiling upload (no dropped connection)."""
        self._write_html(413, _render_intake(store_root=self.store_root, dna_root=self.dna_root))

    def _maybe_care_review(self, store_root, scaffold_root, identity_config, fields):
        """Fire the care-agent review after a complete-profile final save; return its receipt or None.

        The ADR-0033-0035-T8 trigger. Returns the care-review JSON receipt (>= 1 clarifying question
        + the meds-curation state + the "what it is doing" progress status the existing
        `.chat-progress`/`.bar`/`_progressUpdate` surface renders) when a form-field capture just
        completed the profile (T6's `app_shell._intake_complete` predicate) AND a usable no-train
        key + injected client are present — the conservative complete-state superset that satisfies
        both the AC1 final-save and the AC6 material-edit re-trigger with no edge-detection. Returns
        None (the caller falls through to the existing app-shell HTML re-render) when no fields were
        captured, the profile is incomplete, or no key/client is available (the AC5 honest 0-spend
        degrade — the trigger short-circuits BEFORE any model call). The review REUSES the instance
        `self.client` (no second model client) and the instance `_key_available` no-key predicate; a
        review failure is caught and degrades to None so it never drops the request thread (mirrors
        `_do_chat`).
        """
        if not fields or self.client is None or not self._key_available():
            return None
        import functools

        from scripts.serve import care_review
        from scripts.store import store
        from vault.design.templates import app_shell

        resolved_root = store_root if store_root is not None else store.DEFAULT_ROOT
        try:
            if not app_shell._intake_complete(store.read_all(resolved_root)):
                return None
            store_read = functools.partial(store.read, root=resolved_root)
            return care_review.review(
                store_read, client=self.client, key_available=True,
                store_root=resolved_root, scaffold_root=scaffold_root,
                identity_config=identity_config,
            )
        except Exception:
            # Thread survival (mirrors _do_chat): a review failure never drops the request thread —
            # fall through to the existing HTML re-render.
            return None

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

        # CSRF gate (SEC / 55qg): require application/json so a cross-site CORS-simple POST cannot
        # drive the converse spend on the operator's key — refuse before any work (mirrors
        # `_do_generate_plan` / `_do_plan_loop` / `_save_key`; a genuine application/json cross-site
        # POST forces a preflight the server never answers).
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"reply": None, "error": "unsupported content-type"})
            return

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

    def _do_care_chat(self):
        """Run one POST `/care-chat` turn: the profile-aware Care Assistant conversation.

        The POST-unlock care conversation (distinct from `/chat`'s pre-unlock intake elicitation):
        reads a JSON turn body (`{"turn", "conversation"?}`) and runs `care_chat.respond`, which
        re-reads the de-identified `router.summarize` profile server-side and carries it as context so
        the assistant reasons over the whole profile and the conversation (incl. the care-review opening
        questions the client carries back) stays coherent. The ONE outbound model call is the respond's
        `client.converse`. A malformed body or a dispatch/model exception is CAUGHT and answered with a
        degraded response — the request thread is never dropped (mirroring `_do_chat`).
        """
        import json

        # CSRF gate (SEC / 55qg): same forced-spend refusal as `_do_chat` — a non-application/json
        # POST cannot drive `client.converse` on the operator's key. Refuse before any work.
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"reply": None, "error": "unsupported content-type"})
            return

        from scripts.model.client import ModelClient
        from scripts.serve import care_chat, conversation_store

        client = self.client if self.client is not None else ModelClient()
        try:
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            body = json.loads(raw.decode("utf-8")) if raw else {}
            turn_text = body.get("turn", "")
            conversation = body.get("conversation", [])
            thread = body.get("thread") or "care"
            receipt = care_chat.respond(
                turn_text, conversation, client=client, store_root=self.store_root,
                scaffold_root=self.scaffold_root, identity_config=self.identity_config,
            )
            # Persist the turn pair to the gitignored conversation vault so the conversation survives a
            # reload (restored via GET /conversation) — the operator never redoes it. A recording failure
            # must NOT drop the request thread (the reply already succeeded), so it is caught below.
            conv_root = self._conversation_root()
            try:
                conversation_store.record_turn(thread, "user", turn_text, root=conv_root)
                if receipt.get("reply"):
                    conversation_store.record_turn(thread, "assistant", receipt["reply"], root=conv_root)
            except Exception:
                pass
        except Exception:
            # Thread survival (mirrors _do_chat): a malformed body / a dispatch exception must NOT drop
            # the request thread. Answer a degraded response, never a fabricated reply.
            self._write_json(400, {"reply": None, "degraded": True, "reason": "bad request"})
            return
        self._write_json(200, receipt)

    def _conversation_root(self):
        """The conversation vault root for this instance — `<store_root parent>/conversations`.

        Derives from `store_root` so a test/scratch store (`APLUS_DATA_ROOT`) keeps its conversations
        alongside it; None `store_root` (production) -> `conversation_store`'s `vault/conversations/`
        default. The vault is gitignored (PII on-device only, the scaffold posture).
        """
        if self.store_root is None:
            return None
        from pathlib import Path

        return Path(self.store_root).parent / "conversations"

    def _do_get_conversation(self):
        """Answer GET `/conversation?thread=<id>` with the stored conversation turns (the reload restore).

        Reads the thread's conversation from the gitignored conversation vault and returns
        `{"turns": [{"role", "content"}, ...]}` so the SPA can restore a prior conversation on load
        (the operator never redoes it). An unknown/absent thread returns an empty list. Read-only.
        """
        from urllib.parse import parse_qs, urlparse

        from scripts.serve import conversation_store

        query = parse_qs(urlparse(self.path).query)
        thread = (query.get("thread") or ["care"])[0]
        try:
            turns = conversation_store.read_turns(thread, root=self._conversation_root())
        except Exception:
            turns = []
        self._write_json(200, {"turns": turns})

    def _do_confirm_extraction(self):
        """Land the operator-confirmed extracted readings via the unchanged sink.

        Reads a JSON body carrying the operator-confirmed subset (`{"readings": [...]}`, the
        SAME key `/upload`'s review payload returns) and lands ONLY that subset through
        `confirm.land_confirmed` — a CALLER of the UNCHANGED `ingest.manual_entry` sink (no
        second sink/gate/key; the operator-confirm IS the gate). This is the ONLY landing path
        for extracted readings; the `/upload` handler surfaces them and lands 0 (ADR-0030-T3).

        Requires `Content-Type: application/json` (a cross-site CORS-simple text/plain POST is
        rejected 415 BEFORE the body is parsed — the same CSRF gate `_save_key` applies, so a
        forged cross-site POST cannot land attacker-chosen readings). An over-ceiling
        Content-Length is refused 413 BEFORE the body is read (bounded memory). A malformed
        body or a fail-loud land (the all-or-nothing batch's `ValueError`) is CAUGHT and
        answered with a degraded JSON response — the request thread is never dropped
        (mirroring `/chat`'s catch-and-degrade), and no fabricated or partial reading lands.
        """
        import json

        from scripts.serve import confirm

        # CSRF gate (mirrors `_save_key`): require application/json so a cross-site "simple"
        # request (text/plain, no CORS preflight) cannot drive this landing route — a genuine
        # application/json cross-site POST forces a preflight the server never answers.
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"landed": [], "error": "unsupported content-type"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._write_json(400, {"landed": [], "degraded": True, "reason": "bad request"})
            return
        if length > _CONFIRM_MAX_BYTES:
            self._write_json(413, {"landed": [], "error": "too large"})
            return
        try:
            raw = self.rfile.read(length) if length else b""
            body = json.loads(raw.decode("utf-8")) if raw else {}
            readings = body["readings"]
            if not isinstance(readings, list):
                raise ValueError("confirm-extraction: readings must be a list")
            receipt = confirm.land_confirmed(readings, root=self.store_root)
        except Exception:
            # Thread survival: a malformed body / a fail-loud all-or-nothing batch land must
            # NOT kill the request thread. Answer with a degraded response, never a dropped
            # connection — and never a fabricated or partial landed reading.
            self._write_json(400, {"landed": [], "degraded": True, "reason": "bad request"})
            return
        self._write_json(200, {"landed": receipt["store"]})

    def _do_confirm_curation(self):
        """Persist the operator-CONFIRMED meds-curation class tokens (the confirm-when-unsure write-back).

        Reads a JSON body carrying the operator-confirmed de-identified interaction-class tokens
        (`{"classes": [...]}`) and persists ONLY those through `care_review.confirm_curation` — a
        CALLER of the UNCHANGED `store.append` sink (no second sink/gate/key; the operator-confirm
        IS the gate, the SAME disposes-after-gate shape as `_do_confirm_extraction`). This is the
        write-back the leg-2 confirm-when-unsure surface needs: an uncertain curation writes 0
        `rx-interaction-classes` until the operator confirms via this route. Only de-identified
        CLASS tokens cross here — never a raw drug string (the front-end posts the proposed classes).

        Requires `Content-Type: application/json` (a cross-site CORS-simple `text/plain` POST is
        rejected 415 BEFORE the body is parsed — the same CSRF gate `_save_key`/`_do_confirm_extraction`
        apply). An over-ceiling Content-Length is refused 413 BEFORE the body is read (bounded memory).
        A malformed body is CAUGHT and answered with a degraded JSON response — the request thread is
        never dropped (mirroring `_do_confirm_extraction`), and no class token persists on a bad body.
        """
        import json

        from scripts.serve import care_review

        # CSRF gate (mirrors `_do_confirm_extraction`): require application/json so a cross-site
        # "simple" request (text/plain, no CORS preflight) cannot drive this class-write route.
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"confirmed": [], "error": "unsupported content-type"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._write_json(400, {"confirmed": [], "degraded": True, "reason": "bad request"})
            return
        if length > _CONFIRM_MAX_BYTES:
            self._write_json(413, {"confirmed": [], "error": "too large"})
            return
        try:
            raw = self.rfile.read(length) if length else b""
            body = json.loads(raw.decode("utf-8")) if raw else {}
            classes = body["classes"]
            if not isinstance(classes, list):
                raise ValueError("confirm-curation: classes must be a list")
            # Thread the instance identity_config into the value gate (the same H-2 seam /upload
            # threads into persist_capture): a token carrying operator identity/DOB defers the whole
            # batch fail-closed, so a crafted loopback POST cannot land raw PII into the planner token.
            receipt = care_review.confirm_curation(
                classes, store_root=self.store_root, identity_config=self.identity_config
            )
        except Exception:
            # Thread survival: a malformed body / a fail-loud persist must NOT kill the request
            # thread. Answer a degraded response, never a dropped connection — and never a
            # fabricated or half-written class token.
            self._write_json(400, {"confirmed": [], "degraded": True, "reason": "bad request"})
            return
        # Forward the confirm receipt (its `deferred`/`reason` on an identity-bearing batch is honest
        # surfacing, not an error — the request succeeded, nothing was persisted).
        self._write_json(200, {"confirmed": receipt["confirmed"],
                               **({k: receipt[k] for k in ("deferred", "reason") if k in receipt})})

    def _do_confirm_plan_change(self):
        """Apply the operator's explicit confirm/decline of a held large plan re-gen (ADR-0040-T4).

        Reads a JSON body `{"domain","plan_date","decision"}` and applies it through
        `confirm.confirm_plan_change` — flipping the T1 `plan-confirm::` pointer (and, on a confirm,
        firing the deferred care-lane tailoring seam through the instance `tailor_client`). This is
        the operator-facing RELEASE act of the ADR-0040 large-change hold — the stable contract the
        deferred OQ-5 confirm UX calls.

        Requires `Content-Type: application/json` (a cross-site CORS-simple `text/plain` / no-header
        POST is refused 415 BEFORE the body is parsed — the same CSRF gate `_do_confirm_extraction`
        applies, so a forged cross-site POST cannot flip an operator's confirm pointer). An over-
        ceiling Content-Length is refused 413 BEFORE the body is read (bounded memory). A malformed
        body, a missing field, or a present-but-invalid `decision` token (the act's fail-loud
        `ValueError`) is CAUGHT and answered with a degraded 400 JSON — the request thread is never
        dropped (mirroring `_do_confirm_extraction`), and the pointer is never partially flipped.
        """
        import json

        from scripts.serve import confirm

        # CSRF gate (mirrors `_do_confirm_extraction`): require application/json so a cross-site
        # "simple" request (text/plain / no header, no CORS preflight) cannot flip a confirm pointer.
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"domain": None, "decision": None, "error": "unsupported content-type"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._write_json(400, {"domain": None, "decision": None, "degraded": True, "reason": "bad request"})
            return
        if length > _CONFIRM_MAX_BYTES:
            self._write_json(413, {"domain": None, "decision": None, "error": "too large"})
            return
        try:
            raw = self.rfile.read(length) if length else b""
            body = json.loads(raw.decode("utf-8")) if raw else {}
            receipt = confirm.confirm_plan_change(
                body["domain"], body["plan_date"], body["decision"],
                root=self.store_root, tailor_client=self.tailor_client,
            )
        except Exception:
            # Thread survival: a malformed / missing-field body — or the act's fail-loud ValueError on
            # a present-but-invalid decision token — answers a degraded 400, never a dropped thread and
            # never a partial pointer flip.
            self._write_json(400, {"domain": None, "decision": None, "degraded": True, "reason": "bad request"})
            return
        self._write_json(200, {"domain": receipt["domain"], "decision": receipt["decision"]})

    def _do_generate_plan(self):
        """Author + reconcile + record a plan for the plan domains over stored data; answer JSON.

        The in-app trigger for the plan engine — the operator's "Generate plan" press. It gathers
        each `plan_schema.PLAN_DOMAINS` author's envelope through the instance no-train client (the
        ONE model call per domain), then runs the FROZEN cross-domain orchestrator
        (`orchestrate.generate_plans`, CALLED not re-implemented): it reconciles ACROSS domains
        BEFORE recording — the supplement<->peptide additive-AE screen, the nutrition->workout
        energy bounce, the cross-domain-conflict + supplement<->Rx-BPMH holds — and records only the
        survivors via `record_plan`. No reauthor/adjudicator hook is wired here (the agent-harness A'
        path), so a HELD finding stays HELD (the safe default): a supplement+peptide additive-AE pair
        is held, NOT both shipped. The in-app path therefore never RELEASES a hold via a liaison
        override — that needs the care-assistant A' run; the in-app plan is screened, not
        liaison-adjudicated (strictly more conservative, never laxer). The reply is JSON
        `{need_key, results, plan_html}`: `results` maps each domain to `"recorded"` or its honest
        no-plan/hold reason, and `plan_html` is the re-rendered Plan zone the front-end swaps in.

        Resilience + thread survival: each author call is isolated per domain so one domain's failure
        (a ModelCallError degrade, an un-importable model-backend SDK / un-constructable client raising
        ImportError, any unexpected author error) records the others and surfaces that domain's
        honest reason — the run never aborts on one domain. The whole body is wrapped in a
        catch-and-degrade (mirroring `_do_chat` / `_do_confirm_extraction`): a malformed state / an
        unexpected exception answers an honest degraded JSON, never a dropped request thread (no
        RemoteDisconnected).

        CSRF gate (mirrors `_save_key` / `_do_confirm_extraction`): a non-`application/json` POST is
        refused 415 BEFORE any work — a cross-site CORS-simple `text/plain` POST cannot drive forced
        spend on the operator's key + plan writes (a genuine application/json cross-site POST forces a
        preflight the server never answers).

        No-key state: with no USABLE no-train author (`self.client is None` OR no resolvable key — the
        SAME availability check the Profile status reports) it records NOTHING and answers `need_key`
        BEFORE any spend; the engine is never called until a key is connected.
        """
        import datetime
        import functools

        # CSRF gate (SEC): require application/json so a cross-site CORS-simple POST cannot drive
        # plan generation (forced spend + plan writes) — refuse before any work.
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"need_key": False, "results": {}, "plan_html": None,
                                   "error": "unsupported content-type"})
            return

        # No usable no-train author -> the no-key state (BEFORE any spend). `self.client` may be
        # absent (test-built) OR present-but-keyless (production: a live ModelClient with no resolvable
        # key); either way route the operator to connect their key, engine uncalled.
        if self.client is None or not self._key_available():
            self._write_json(200, {"need_key": True, "results": {}, "plan_html": None})
            return

        try:
            from scripts.model.client import ModelCallError
            from scripts.plan import orchestrate, router
            from scripts.plan.generate_plan import AUTHOR_CALL_FAILED
            from scripts.serve import care_chat, plan_loop
            from scripts.serve.intake_aggregate import normalize_author_output
            from scripts.store import plan_schema, store
            from vault.design.templates import app_shell

            store_root = self.store_root if self.store_root is not None else store.DEFAULT_ROOT
            # The reader is instance-root pre-bound (the router.summarize caller contract). Record
            # under today so the plan resolves as today's on the Plan screen (date equality).
            store_read = functools.partial(store.read, root=store_root)
            today = datetime.date.today().isoformat()

            # OPTION 2 (ADR-0043-T3): derive the de-id-safe operator surface and NARROW the author
            # loop to the active ∩ renderable subset (not the closed grown PLAN_DOMAINS). The composed
            # cross-domain-safety delegation (orchestrate.generate_plans — the gate Leg 1 for this
            # front door) is PRESERVED and promotes the active subset thin as today; a rich domain
            # active in the surface is folded into the comprehensive version by Leg 2 (never the thin
            # renderable-validator path).
            summary = router.summarize(store_read)
            active = plan_loop.active_plan_domains(summary)
            renderable_active = sorted(active & set(plan_schema.RENDERABLE_DOMAINS))

            # Gather each active domain's author envelope through the no-train client (the ONE model
            # call per domain), isolated per domain: a ModelCallError degrades to the honest
            # author-call-failed reason; an un-importable SDK / un-constructable client degrades to
            # an honest model-backend-unavailable reason; any other unexpected author error degrades
            # THAT domain — never a thread drop, never an aborted run.
            authors = {}
            author_errors = {}
            for domain in renderable_active:
                try:
                    # Path B (the in-app /generate-plan front door): normalize the model author
                    # envelope's scalar-contract rec fields UPSTREAM of the frozen composer, exactly
                    # as the cadence path does at build_dispatch (bead mk0i — a list/dict rec field
                    # otherwise crashes the frozen generate_plans composer mid-run for ALL domains).
                    authors[domain] = normalize_author_output(self.client.author(domain, summary))
                except ModelCallError:
                    author_errors[domain] = AUTHOR_CALL_FAILED
                except (ImportError, ModuleNotFoundError):
                    author_errors[domain] = "model-backend-unavailable"
                except Exception as exc:
                    author_errors[domain] = f"error: {type(exc).__name__}"

            # Reconcile across domains BEFORE recording (the FROZEN orchestrator, CALLED). No
            # reauthor/adjudicator hook is wired (the agent-harness A' path), so a held finding stays
            # HELD — the safe default: a supplement+peptide additive-AE pair is held, not both shipped.
            outcome = orchestrate.generate_plans(authors, store_read, store_root, plan_date=today)

            results = {}
            for domain in renderable_active:
                if domain in author_errors:
                    results[domain] = author_errors[domain]
                    continue
                record = outcome["results"].get(domain)
                results[domain] = (
                    "recorded" if record and record["recorded"] else ((record or {}).get("reason") or "no-plan")
                )

            # Leg 2 (OPTION 2 — ADDITIVE, gated by the pass): once the reconcile promoted >=1 domain,
            # the care-agent synthesize step records ONE comprehensive version (the gate-cleared
            # programs + any active rich domain authored via the no-train client, reconciled through
            # the always-on floors) — ON TOP of the KEPT thin write. When nothing promoted, no record.
            if any(record.get("recorded") for record in outcome["results"].values()):
                def _author_rich(domain, _summary=summary):
                    try:
                        return normalize_author_output(self.client.author(domain, _summary))
                    except Exception:
                        return None
                care_chat.synthesize(active, outcome, _author_rich, store_read,
                                     on_date=today, root=store_root)

            plan_html = app_shell._plan_zone(store.read_all(store_root), today, store_root)
            self._write_json(200, {"need_key": False, "results": results, "plan_html": plan_html})
        except Exception:
            # Thread survival (mirrors _do_chat / _do_confirm_extraction): a malformed state / an
            # unexpected exception (an un-importable SDK at summary time, a fail-loud record rejection,
            # the PII gate raise) must NOT drop the request thread. Answer an honest degraded response
            # — never a RemoteDisconnected, never a fabricated plan.
            self._write_json(200, {"need_key": False, "results": {}, "plan_html": None,
                                   "degraded": True, "reason": "could not generate plan"})

    def _do_plan_loop(self):
        """Fire one automated plan-evolution loop tick through the full-composition front door; answer JSON.

        The cadence/manual loop trigger (ADR-0036-T1). It drives `plan_loop.regenerate` with the
        instance loop `dispatch` + `deid_client` seams (mirroring the injectable `self.client`
        pattern so the fixture E2E runs at 0 live spend) over `self.store_root` — binding the trigger
        to `run_orchestrated` -> `plan_driver.drive` -> the composed `gate_dispatch` + the five
        `orchestrate` cross-domain holds. It is DISTINCT from `_do_generate_plan` and does NOT call
        it: the loop path never reaches the screened-only route (the anti-degradation guard). The run
        result is answered as JSON.

        CSRF gate (mirrors `_save_key` / `_do_generate_plan`): a non-`application/json` POST is
        refused 415 BEFORE any work — a cross-site CORS-simple `text/plain` POST cannot drive the
        highest-spend loop tick (every specialist + judge + lens dispatch) on the operator's key (a
        genuine application/json cross-site POST forces a preflight the server never answers).

        Seams-absent state (mirrors `_do_generate_plan`'s no-key early-return): when the loop
        `dispatch`/`deid_client` seams are absent — the standalone-server posture, since production
        `main()` supplies no subscription runtime (bead 3ge1) — answer a DISTINCT honest
        `loop-dispatch-unavailable` degraded reason before any work, never the generic catch-all.

        Thread survival (mirrors `_do_chat` / `_do_generate_plan`): a malformed state / an unexpected
        exception answers an honest degraded JSON, never a dropped request thread.
        """
        from scripts.serve import plan_loop
        from scripts.store import store

        # CSRF gate (SEC): require application/json so a cross-site CORS-simple POST cannot drive the
        # loop tick (forced spend across every specialist + judge + lens) — refuse before any work.
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"results": {}, "error": "unsupported content-type"})
            return

        # Honest degradation (bead 3ge1): the loop's A' aggregate dispatch is a subscription-session
        # runtime the standalone `python -m scripts.serve` process does NOT host (ADR-0036
        # Consequences), so production `main()` supplies no `loop_dispatch`/`loop_deid_client`. Answer
        # a DISTINCT honest reason — never fabricate a dispatch, never the generic catch-all, never a
        # confusing inner deid-call-failed shape from driving `regenerate` with absent seams.
        if self.loop_dispatch is None or self.loop_deid_client is None:
            self._write_json(200, {"results": {}, "degraded": True,
                                   "reason": "loop-dispatch-unavailable"})
            return

        store_root = self.store_root if self.store_root is not None else store.DEFAULT_ROOT
        try:
            result = plan_loop.regenerate(
                store_root, dispatch=self.loop_dispatch, deid_client=self.loop_deid_client,
            )
            self._write_json(200, result)
        except Exception:
            self._write_json(200, {"results": {}, "degraded": True, "reason": "could not run plan loop"})

    def _key_available(self):
        """Whether a no-train key resolves at runtime — the Profile 'connected' availability check.

        The SINGLE key-availability predicate shared by the Profile status (GET /settings/key)
        and the POST /generate-plan no-key guard, so the two cannot silently diverge: a key is
        available iff `key_source.resolve()` (or the injected `key_resolver`) returns without
        raising `KeyUnavailableError`. Reports presence ONLY — it never reads the secret value.
        """
        from scripts.model import key_source

        resolver = self.key_resolver if self.key_resolver is not None else key_source.resolve
        try:
            resolver()
            return True
        except key_source.KeyUnavailableError:
            return False

    def _key_status(self):
        """Write JSON `{connected: bool}` — whether a no-train key resolves at runtime.

        Reports ONLY whether a key is present (via `_key_available`) — never the value. An
        absent key is the normal not-connected path, not an error. Lets the Profile screen
        show Connected / Not connected without ever reading the secret.
        """
        self._write_json(200, {"connected": self._key_available()})

    def _save_key(self):
        """Read a JSON `{api_key}` body and store it in the OS keychain.

        The key is written ONLY to the keychain (via `key_source.store`) — never logged,
        echoed in the response, or written to a file. The response carries no key value,
        only `{ok, connected}`. An empty key is a 400; a keychain write failure is a 500
        with a constant message. The request thread is never dropped (mirrors `/chat`'s
        catch-and-degrade posture). Accepted over loopback only, so the secret never
        leaves the machine (ADR-0013 transport posture).
        """
        import json

        from scripts.model import key_source

        # Require application/json so a cross-site "simple" request (text/plain, which
        # triggers no CORS preflight) cannot drive this secret-write route: a genuine
        # application/json cross-site POST forces a preflight the server never answers,
        # so the browser blocks it (SEC-001 — CSRF on the first secret-write surface).
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"ok": False, "error": "unsupported content-type"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._write_json(400, {"ok": False, "error": "bad request"})
            return
        if length > _SETTINGS_MAX_BYTES:
            self._write_json(413, {"ok": False, "error": "too large"})
            return
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8")) if raw else {}
        except (ValueError, UnicodeDecodeError):
            self._write_json(400, {"ok": False, "error": "bad request"})
            return
        # A top-level non-object JSON body (123 / [] / "x") or a non-string api_key has no
        # .get / .strip — guard both so a malformed body is a 400, never an uncaught
        # AttributeError that drops the request thread (BUG-001; the catch-and-degrade
        # posture this docstring already promises).
        if not isinstance(body, dict):
            self._write_json(400, {"ok": False, "error": "bad request"})
            return
        api_key = body.get("api_key")
        key = api_key.strip() if isinstance(api_key, str) else ""
        if not key:
            self._write_json(400, {"ok": False, "error": "empty key"})
            return
        store = self.key_store if self.key_store is not None else key_source.store
        try:
            store(key)
        except (ValueError, key_source.KeyStoreError):
            # Constant message — never the key. A store failure must not leak the secret.
            self._write_json(500, {"ok": False, "error": "could not store key"})
            return
        # Make the just-saved key resolvable in THIS running server immediately: resolve()
        # checks the env var first, so the chat works right after Save without a keychain
        # read (a backgrounded server can otherwise need a one-time keychain-access prompt
        # the operator can't approve). The key lives in process memory only — never logged,
        # returned, or filed; the keychain write is the cross-restart persistence.
        import os

        os.environ[key_source.ENV_VAR] = key
        self._write_json(200, {"ok": True, "connected": True})

    def _tracker_status(self):
        """Write JSON `{sources: {<source>: bool, ...}}` — per-source connected booleans, never a value.

        Reports, for each WIRED tracker source, whether its OAuth credential is EFFECTIVELY present
        (`oauth_pull._read_oauth_credential(source) is not None` — the reader's strip/blank-collapse
        semantics, so a whitespace-only stored value reports `false`, matching what the pull actually
        sees, and routing status through `_oauth_service_name` at one derivation site). Reports ONLY
        booleans — never a token value (mirrors `_key_status`'s present-only contract). The wired
        source set is read at REQUEST time from `oauth_pull`'s manifests (a function-local import) so
        it stays data-driven, not a hand-copied list.
        """
        from scripts.ingest import oauth_pull

        sources = {
            source: oauth_pull._read_oauth_credential(source) is not None
            for source in oauth_pull._MANIFESTS
        }
        self._write_json(200, {"sources": sources})

    def _save_tracker_token(self):
        """Read a JSON `{source, token}` body and store the per-source OAuth token via `secret_store`.

        The N-per-source companion to `_save_key`: the token is written ONLY to the secret store (via
        `secret_store.set_secret`) into the SAME `a-plus-maxing-<source>-oauth` item `oauth_pull`'s
        default reader reads — never logged, echoed in the response, or written to a file. The gate
        order mirrors `_save_key` EXACTLY for the shared gates, with ONE new gate — source validation
        — inserted between shape and token: the SEC-001 `application/json` CSRF gate FIRST (before the
        body is read), then the 16-KiB body ceiling, then JSON-parse/shape, then EXACT-membership
        source validation (fail-closed), then strip/empty-reject, then the write. Every error body is
        `{ok: false, error: <constant>}` and NO surface carries the token value (NFR-3). Accepted over
        loopback only; the request thread is never dropped.
        """
        import json

        # CSRF (SEC-001, byte-mirrors `_save_key`): a non-`application/json` POST is refused 415 BEFORE
        # the body is read — the exact ctype normalization so `application/json; charset=utf-8` passes
        # and a naive `!=` false-415 is avoided. A cross-site CORS-simple `text/plain` POST is refused;
        # a genuine cross-site `application/json` POST forces a preflight the server never answers.
        ctype = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if ctype != "application/json":
            self._write_json(415, {"ok": False, "error": "unsupported content-type"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._write_json(400, {"ok": False, "error": "bad request"})
            return
        if length > _SETTINGS_MAX_BYTES:
            self._write_json(413, {"ok": False, "error": "too large"})
            return
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8")) if raw else {}
        except (ValueError, UnicodeDecodeError):
            self._write_json(400, {"ok": False, "error": "bad request"})
            return
        if not isinstance(body, dict):
            self._write_json(400, {"ok": False, "error": "bad request"})
            return
        # Read via `.get` (never subscript): an ABSENT source/token is None, not an uncaught KeyError
        # that drops the request thread. A non-str source/token (incl. None-from-absent) is a 400 —
        # the source isinstance guard also makes the membership check below safe against an unhashable
        # source (`["whoop"] in <set>` would raise TypeError).
        source = body.get("source")
        token = body.get("token")
        if not isinstance(source, str) or not isinstance(token, str):
            self._write_json(400, {"ok": False, "error": "bad request"})
            return

        from scripts.ingest import oauth_pull

        # Source validation (fail-closed; sec LOW-1): EXACT membership in the wired manifest set — no
        # case-folding, no normalization (a case/homoglyph variant simply misses -> 400). Read at
        # REQUEST time so it stays data-driven. The SAME validated string is passed VERBATIM to the
        # service-name derivation, so the write lands in the item it validated — closing the
        # service-name-injection surface (an unvalidated source could write an arbitrary keyring item).
        if source not in oauth_pull._MANIFESTS:
            self._write_json(400, {"ok": False, "error": "unknown source"})
            return
        token = token.strip()
        if not token:
            self._write_json(400, {"ok": False, "error": "empty token"})
            return

        from scripts import secret_store

        # The write goes DIRECTLY through `secret_store` into the SAME item `oauth_pull`'s default
        # reader reads (`_oauth_service_name` is MANDATED — one derivation site, no literal here).
        try:
            secret_store.set_secret(oauth_pull._oauth_service_name(source), token)
        except secret_store.KeyStoreError:
            # Constant message — never the token, and it does NOT assert the token is unstored as a
            # certainty (`set_secret` also raises when the write SUCCEEDED but stale fallback residue
            # could not be cleared — the T2-F2 clear-fail case).
            self._write_json(500, {"ok": False, "error": "could not store token"})
            return
        self._write_json(200, {"ok": True, "connected": True})

    def _write_json(self, status, obj):
        """Write a JSON response body (the `/chat` turn-receipt response-write site)."""
        import json

        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _write_html(self, status, html):
        """Write an HTTP response with the HTML body (the single response-write site).

        `Cache-Control: no-store` is REQUIRED, not cosmetic: the served page IS the app (a single
        inline-asset document regenerated fresh on every GET). Without it the stdlib server sends no
        cache directives, so the browser is free to serve a STALE cached copy on refresh — running old
        JavaScript (so the wizard's localStorage autosave never runs and typed work is lost on reload)
        and old markup (no pre-fill / no already-loaded note). The operator saw exactly that. no-store
        forces every load/refresh to fetch the current document so a code update is never masked.
        """
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        """Silence the default per-request stderr access log."""


def build_server(port, *, store_root=None, dna_root=None, scaffold_root=None,
                 identity_config=None, client=None, key_resolver=None, key_store=None,
                 loop_dispatch=None, loop_deid_client=None):
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
    # The key seams are CALLABLES held as class attributes — wrap in staticmethod so
    # `self.key_resolver()` / `self.key_store(key)` call them plainly instead of binding
    # `self` as a leading argument. (store_root/client are data, not callables, so they
    # need no wrap; None passes through to the production key_source defaults.)
    handler = type("BoundIntakeRequestHandler", (IntakeRequestHandler,),
                   {"store_root": store_root, "dna_root": dna_root,
                    "scaffold_root": scaffold_root, "identity_config": identity_config,
                    "client": client,
                    "loop_deid_client": loop_deid_client,
                    "loop_dispatch": staticmethod(loop_dispatch) if loop_dispatch is not None else None,
                    "key_resolver": staticmethod(key_resolver) if key_resolver is not None else None,
                    "key_store": staticmethod(key_store) if key_store is not None else None})
    return ThreadingHTTPServer((_LOOPBACK, port), handler)
