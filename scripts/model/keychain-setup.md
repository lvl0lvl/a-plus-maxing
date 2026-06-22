# No-Train API Key — Runtime Setup

The model client (`scripts/model/client.py`) resolves the no-train API key at **runtime**
via `key_source.resolve()`. The key is **never** stored in this repo — the repo is PUBLIC.
`resolve()` reads two sources, in order:

1. the `APLUS_NOTRAIN_API_KEY` environment variable, then
2. the macOS keychain item under service name `aplus-notrain-api-key`.

If neither yields a key, `resolve()` raises `KeyUnavailableError` fail-loud. Set up **one**
of the two below.

## Option A — environment variable (CI / a shell session)

Export the key in the shell that runs the app (a real key replaces `<YOUR_KEY>`; do not
paste a real key into any tracked file):

```sh
export APLUS_NOTRAIN_API_KEY='<YOUR_KEY>'
```

## Option B — macOS keychain (persistent, recommended for a local operator)

Store the key once in the login keychain under the service name the key source reads:

```sh
security add-generic-password \
  -a "$USER" \
  -s aplus-notrain-api-key \
  -w '<YOUR_KEY>' \
  -U
```

`key_source.resolve()` then fetches it at call time with:

```sh
security find-generic-password -w -s aplus-notrain-api-key
```

To rotate the key, re-run the `add-generic-password` command (the `-U` flag updates the
existing item). To remove it:

```sh
security delete-generic-password -s aplus-notrain-api-key
```

## Verify (no live API call)

`resolve()` does not call the API — it only returns the key string. Confirm it resolves:

```sh
APLUS_NOTRAIN_API_KEY='<YOUR_KEY>' \
  .venv/bin/python -c "from scripts.model.key_source import resolve; print(bool(resolve()))"
```

Expected output: `True`. A missing key raises `KeyUnavailableError` naming this runbook.
