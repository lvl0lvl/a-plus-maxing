# Clone Init — From a Fresh Clone to a Fillable Instance

This is the operator-facing guide for taking a fresh `git clone` of a-plus-maxing
to a fillable, PII-free local instance. A clone ships with empty `status: scaffold`
pages and no operator data — every instance is independent, local, and single-operator.

## From git clone to a fillable instance

After cloning the repository, run the clone-init step once from the clone root:

```bash
python3 -c "from scripts.clone import init_instance; init_instance.run()"
```

This initializes the local store under `vault/store/` (empty and readable — no
readings yet) and surfaces the empty `status: scaffold` pages in their unfilled
state. It makes no network call and reads nothing outside the clone. After init,
fill the scaffold pages and enter your own readings; the instance generates a
dashboard from your local inputs alone.

### The PII pre-push backstop

Init copies `.claude/hooks/pre-push-pii-scan.sh` into your clone's
`.git/hooks/pre-push`. It scans the files in each push range for operator PII
(your name on health-data paths, your contact tokens anywhere, store-shaped
content) and blocks a push that would carry any to the remote — defense-in-depth
behind the agent-session commit hook, for pushes from a plain terminal or IDE.

- It **never overwrites** a pre-push hook you wrote yourself (it keys on an
  ownership marker); re-running init refreshes only its own prior copy.
- `git push --no-verify` bypasses it (as it does any pre-push hook).
- To enable contact detection, copy `vault/meta/operator-contact.txt.example` to
  `vault/meta/operator-contact.txt` (gitignored) and add your real email/handles.

### Your entered data is excluded from version control — keep a separate local backup

Everything you enter after init — your readings under `vault/store/` and your
filled scaffold values — is **excluded from version control** by the repository's
`.gitignore`. This is deliberate: a clone carries no operator data, so the
repository never holds anyone's personal health information.

The consequence is that git is **not** a backup of your entered data. Because the
store and filled scaffolds are never committed, they have no version-control
history or backup. **Keep a separate local backup of your `vault/store/` data and
filled scaffolds** — if the working copy is lost, that data cannot be recovered
from git.

## The project issue tracker (`.beads/`) — dev tooling, not part of your instance

The repository ships `.beads/` — the a-plus-maxing **dev issue tracker** (the
`a-plus-maxing-*` issues that track building the project, not your health data). A
fresh clone carries the tracked issue records (`.beads/issues.jsonl`) but **not** the
SQLite database (`.beads/*.db` is gitignored): the database is a per-machine local
cache rebuilt from the tracked JSONL, never shared between clones.

If you are running a-plus-maxing as your own health instance, you can **ignore
`.beads/` entirely** — `init_instance.run()` does not touch it, and nothing in the
fillable instance depends on it.

If you are contributing and want the issue tracker, run **`bd init --from-jsonl`**
once from the clone root to build the local database from the tracked records. Most
`bd` commands (`bd list`, `bd ready`, `bd create`) also rebuild the database
automatically on first use; only `bd sync --flush-only` requires the database to
exist first (it is the one command that does not auto-import, so it errors with
`no beads database found` on a never-initialized clone).
