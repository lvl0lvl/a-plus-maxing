# A+ Maxing

A **local-first, single-operator** health-intelligence system. It ingests your own health
data (wearable exports, labs, DNA), tracks it, and generates a source-grounded,
physician-ready plan — all on your machine.

> **Your data never leaves your computer.** Ingestion is plain local code: your files are
> parsed on your machine into a local store. Nothing is uploaded, and the model is never in
> the loading path. (See **[Privacy](#privacy)**.)

This repo is the **engine + empty scaffolds** — it carries **zero operator data**. Every
clone is an independent instance: you load your own data locally, and no clone can read
another's. That's what makes it safe for several people to test at once — each person runs
their own instance with their own data.

---

## Quickstart

```bash
# 1. clone + create the per-instance Python env
git clone <repo-url> a-plus-maxing && cd a-plus-maxing
python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt

# 2. initialize your local instance (creates the gitignored store + installs the PII pre-push guard)
.venv/bin/python -c "from scripts.clone import init_instance; init_instance.run()"

# 3. load your data (see below) — local only, nothing uploaded

# 4. render a screen and open it
.venv/bin/python -m scripts.generate.generate intake      # the "Build your plan" intake screen
open vault/artifacts/generated/intake.html
```

Detail on the clone→instance step: **[docs/clone-init.md](docs/clone-init.md)**.

---

## Loading your data

One command per export. Each is parsed **locally** and written only to your gitignored
local store/dropzone — no upload, no model, no network.

```bash
# Apple Health — Health app → profile → "Export All Health Data" → unzip → export.xml
.venv/bin/python -m scripts.ingest /path/to/export.xml

# DNA — your 23andMe export, straight from the zip (validated + landed; never analyzed at load time)
.venv/bin/python -m scripts.ingest /path/to/23andme.zip

# the source is auto-detected from the file; force it with --source if needed
.venv/bin/python -m scripts.ingest /path/to/data --source healthkit
```

Each run prints exactly what landed (metrics + date ranges for a wearable; the variant count
for DNA) and ends with *"parsed locally — nothing was uploaded."*

**What's wired today:** Apple Health (`export.xml`) → the time-series store; DNA
(`.zip`/`.txt`) → the gitignored `vault/dna/raw/` dropzone. Whoop / Oura / Garmin adapters
exist (`--source whoop|oura|garmin`). Labs ingestion and the DNA clinical-variant *analysis*
are separate, later steps.

### The intake screen

`.venv/bin/python -m scripts.generate.generate intake` renders the 6-step **Build your plan**
wizard to `vault/artifacts/generated/intake.html`. Step 1's "Link your documents" cards are
**live** — they show what you've loaded (✓ with counts + date range) and the exact command to
load what you haven't.

---

## Privacy

Two boundaries, both architectural (not policy promises):

1. **Loading never touches the model or the network.** The ingestion path is plain Python —
   your file → a local parser → a local file. There is no LLM call and no network egress in
   that path (enforced by an egress-guard test). The only way data reaches a model is the
   *plan-reasoning* step, which runs over a **de-identified summary** on a commercial
   **no-train, non-retained** API path — never your raw data (ADR-0001).
2. **Your data is never committed.** Your readings (`vault/store/`), DNA (`vault/dna/raw/`),
   labs (`vault/labs/raw/`), and filled profile values are all gitignored, and a commit-time
   hook + a pre-push backstop refuse to let operator data into the repo (ADR-0005). The public
   repo stays operator-agnostic.

**No git backup.** Because your data is deliberately never committed, it has no
version-control history — **keep your original export files** as the source of truth.

---

## For testers

Each tester clones the repo and runs their **own** instance: clone → `init_instance` → load
**your own** data → view. There is no shared server, no accounts, and **zero cross-instance
data paths** — no one can see anyone else's data. The repo you cloned stays clean; your data
lives only in your gitignored local store.
