# No-Train API Key — Runtime Setup

## Prerequisite — install the model SDK (live run only)

The `anthropic` SDK is intentionally NOT in `requirements.txt` — the test suite runs with
it absent so no test can make a live model call (0-live-spend). Before the operator-present
live run, install it into the instance `.venv`:

```sh
.venv/bin/python -m pip install anthropic==0.112.0
```

Without it, `converse`/`deidentify` fail closed (`ModelCallError`) — the chat degrades but
spends nothing.

The model client (`scripts/model/client.py`) resolves the no-train API key at **runtime**
via `key_source.resolve()`. The key is **never** stored in this repo — the repo is PUBLIC.
`resolve()` reads two sources, in order:

1. the `ANTHROPIC_API_KEY` environment variable (the anthropic SDK's native var and the
   operator's documented injection var), then
2. the macOS keychain item under service name `a-plus-maxing-api-key`.

If neither yields a key, `resolve()` raises `KeyUnavailableError` fail-loud. Set up **one**
of the options below.

## Option 0 — in-app, no terminal (recommended for alpha testers)

Open **Profile** in the running app and paste your key into "API connection" → Save. The
app writes it to the keychain item `a-plus-maxing-api-key` for you (the same item `resolve()`
reads). Find it later in Keychain Access by searching `a-plus-maxing-api-key`. Note: if the
`ANTHROPIC_API_KEY` env var is also set in the shell that launched the app, it takes
precedence over this keychain item.

## Option A — environment variable (CI / a shell session)

Export the key in the shell that runs the app. The operator's documented injection reads
the key straight out of the `a-plus-maxing-api-key` keychain item (no real key in any tracked
file):

```sh
export ANTHROPIC_API_KEY=$(security find-generic-password -s "a-plus-maxing-api-key" -w)
```

(or, for CI, export a literal: `export ANTHROPIC_API_KEY='<YOUR_KEY>'`.)

## Option B — macOS keychain (persistent, recommended for a local operator)

Store the key once in the login keychain under the service name the key source reads (the
operator's existing item is `a-plus-maxing-api-key`):

```sh
security add-generic-password \
  -a "$USER" \
  -s a-plus-maxing-api-key \
  -w '<YOUR_KEY>' \
  -U
```

`key_source.resolve()` then fetches it at call time with:

```sh
security find-generic-password -w -s a-plus-maxing-api-key
```

To rotate the key, re-run the `add-generic-password` command (the `-U` flag updates the
existing item). To remove it:

```sh
security delete-generic-password -s a-plus-maxing-api-key
```

## Security residuals (accepted)

The in-app save (Option 0) writes the keychain item with `security add-generic-password -U -A`.
Two residuals are accepted deliberately on the single-operator local machine:

- **`-A` (allow-all ACL).** The item is readable by any process running as the operator with
  no keychain-access prompt. This is intentional: the backgrounded server resolves the key
  without a user present to approve an interactive prompt. The accepted threat is that
  same-user malware could read the no-train key without a prompt; the blast radius is one
  operator's machine and one no-train API key. A future hardening is a `-T`-scoped ACL granting
  only the specific reader — deferred because it risks reintroducing the read prompt on headless
  resolves. (Option B's manual command omits `-A`, so a terminal-stored key keeps the default,
  prompt-on-foreign-read ACL.)
- **Key as subprocess argv.** The value is passed as the `-w <key>` argument to `security`, so
  for that process's brief lifetime the plaintext key is visible in the process list (`ps -axww`)
  to other local processes. This is inherent to `security add-generic-password` (it has no stdin
  password path; omitting `-w` prompts interactively, which the backgrounded server cannot
  answer). The exposure window is the duration of one `security` invocation.

## Verify (no live API call)

`resolve()` does not call the API — it only returns the key string. Confirm it resolves:

```sh
ANTHROPIC_API_KEY=$(security find-generic-password -s "a-plus-maxing-api-key" -w) \
  .venv/bin/python -c "from scripts.model.key_source import resolve; print(bool(resolve()))"
```

Expected output: `True`. A missing key raises `KeyUnavailableError` naming this runbook.
