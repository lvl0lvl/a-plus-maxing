"""DNA raw-export landing — drop a 23andMe-format genotype file into the local dropzone.

DNA is NOT a time-series reading (it is a one-time genotype table, not an `(item,
timepoint, source, value)` measurement), so it does NOT flow through `ingest.run` /
the `vault/store/` store. Instead `land(source_file, dna_root)` validates that the
file is a genotype table and copies it into the gitignored `vault/dna/raw/` dropzone
(ADR-0005) — the operator owns the file; the read is one-way + local (unzip + line
scan only): no model step, no network call. The downstream clinical-SNP ANALYSIS
(variants of note -> profile + `vault/dna/analysis.md`, the LM-03 landmark) is a
SEPARATE, sensitive step that reads the landed file; landing only gets the file
safely into the instance.

The validation is the feature: a real 23andMe raw export is a tab-separated table of
`rsid<TAB>chromosome<TAB>position<TAB>genotype` rows under a `#`-comment header. A
file with no genotype-shaped row raises (fail-loud — a wrong file is not silently
landed). Only the variant COUNT is surfaced, never genotype content.
"""

import re
import shutil
import zipfile
from pathlib import Path

# A 23andMe raw-data genotype row: rsid (rs... or 23andMe-internal i...), chromosome
# (1-22 / X / Y / MT), integer position, genotype (1-2 calls from A/C/G/T, D/I for
# indels, - for a no-call). Tab-separated. The header rows start with `#`.
_GENOTYPE_ROW = re.compile(r"^(rs|i)\w+\t(?:\d{1,2}|X|Y|MT)\t\d+\t[ACGTDI\-]{1,2}$")


def _looks_like_genotype(text_lines):
    """Return the count of genotype-shaped rows, scanning lines without holding content.

    A file is a genotype table iff at least one line matches the 23andMe row shape.
    Counts every matching row (the variant count) and ignores `#`-comment/blank lines.

    Args:
        text_lines (Iterable[str]): The file's lines (without trailing newlines).

    Returns:
        (int) The number of genotype-shaped rows found (0 means not a genotype file).
    """
    count = 0
    for line in text_lines:
        if _GENOTYPE_ROW.match(line.rstrip("\n")):
            count += 1
    return count


def _genotype_member(zf):
    """Return the name of the single genotype `.txt` member in an open zip, or raise.

    Skips directories and macOS `__MACOSX` resource forks; validates each candidate
    `.txt` member by its genotype shape and returns the first that validates.

    Args:
        zf (zipfile.ZipFile): The open export zip.
    """
    for name in zf.namelist():
        if name.endswith("/") or name.startswith("__MACOSX") or not name.endswith(".txt"):
            continue
        with zf.open(name) as member:
            head = (member.read(65536).decode("utf-8", "replace")).splitlines()
        if _looks_like_genotype(head):
            return name
    raise ValueError(
        "no 23andMe-format genotype .txt found inside the zip "
        "(expected tab-separated rsid/chromosome/position/genotype rows)"
    )


def land(source_file, dna_root):
    """Validate a 23andMe-format DNA export and land it in the local `dna_root` dropzone.

    Accepts the export `.zip` (the genotype `.txt` is extracted from it) or the raw
    `.txt` directly. Validates the genotype-table shape (fail-loud on a non-genotype
    file), copies the validated file into `dna_root` under its basename, and returns
    the landed path + the variant count. No genotype content is read into the return
    or logged; the read is one-way, local, model-free, network-free.

    Args:
        source_file (str | Path): Path to the operator's DNA export (`.zip` or `.txt`).
        dna_root (str | Path): The gitignored DNA dropzone (production: `vault/dna/raw/`).

    Returns:
        (dict) `{"path": Path, "variants": int, "name": str}` — the landed file path,
            the genotype-row count, and the landed basename.
    """
    source = Path(source_file)
    dest_root = Path(dna_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as zf:
            member = _genotype_member(zf)
            landed = dest_root / Path(member).name
            with zf.open(member) as src, open(landed, "wb") as out:
                shutil.copyfileobj(src, out)
    else:
        with open(source, encoding="utf-8", errors="replace") as fh:
            variants = _looks_like_genotype(fh)
        if not variants:
            raise ValueError(
                f"{source.name} is not a 23andMe-format genotype file "
                "(no tab-separated rsid/chromosome/position/genotype rows found)"
            )
        landed = dest_root / source.name
        if landed.resolve() != source.resolve():
            shutil.copyfile(source, landed)

    with open(landed, encoding="utf-8", errors="replace") as fh:
        variants = _looks_like_genotype(fh)
    return {"path": landed, "variants": variants, "name": landed.name}
