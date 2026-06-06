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
