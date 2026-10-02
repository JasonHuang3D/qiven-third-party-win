"""verify_provenance.py — singleton provenance digest verifier (gate task).

Law: qiven-devkit docs/engineering/third-party-dependencies.md v2
(section 7). Verifies every packages/*/PROVENANCE.yaml: per-file SHA-256
inventory, no unlisted files, CMakeLists.txt present per package.
Zero-dependency (strict-subset parser) so any workspace python runs it.
"""

from __future__ import annotations

import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGES = ROOT / "packages"

EXPECTED_SCHEMA = "qiven-third-party-provenance-v2"


def parse_provenance(text: str) -> dict:
    """Strict subset parser (same law as consumers' verifiers): flat
    key:value, one archive_digest block, files: items; fails closed."""
    record: dict = {"files": []}
    section = None
    item = None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indent == 0:
            if stripped == "files:":
                section, item = "files", None
                continue
            if stripped == "archive_digest:":
                section, item = "archive_digest", None
                record["archive_digest"] = {}
                continue
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                record[key.strip()] = value.strip().strip("'\"")
                section, item = None, None
                continue
            raise ValueError(f"line {lineno}: unparseable {stripped!r}")
        if indent == 2 and stripped.startswith("- "):
            if section != "files":
                raise ValueError(f"line {lineno}: list item outside files: {stripped!r}")
            body = stripped[2:]
            key, _, value = body.partition(":")
            if key.strip() != "path":
                raise ValueError(f"line {lineno}: files item must start with path: {body!r}")
            item = {"path": value.strip()}
            record["files"].append(item)
            continue
        if indent >= 2 and ":" in stripped and not stripped.startswith("- "):
            key, _, value = stripped.partition(":")
            key, value = key.strip(), value.strip().strip("'\"")
            if section == "files" and item is not None:
                item[key] = value
            elif section == "archive_digest":
                record["archive_digest"][key] = value
            else:
                raise ValueError(f"line {lineno}: stray field {stripped!r}")
            continue
        raise ValueError(f"line {lineno}: unparseable {stripped!r}")
    return record


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not PACKAGES.is_dir():
        print("[ OK ] third-party-verify: no packages/ (empty singleton)")
        return 0
    failures: list[str] = []
    checked = 0
    packages = sorted(p for p in PACKAGES.iterdir() if p.is_dir())
    if not packages:
        failures.append("packages/ exists but is empty")
    for package in packages:
        provenance_path = package / "PROVENANCE.yaml"
        if not provenance_path.is_file():
            failures.append(f"{package.name}: missing PROVENANCE.yaml")
            continue
        if not (package / "CMakeLists.txt").is_file():
            failures.append(f"{package.name}: missing CMakeLists.txt (required for every class)")
        try:
            record = parse_provenance(provenance_path.read_text(encoding="utf-8"))
        except ValueError as error:
            failures.append(f"{provenance_path}: {error}")
            continue
        if record.get("schema") != EXPECTED_SCHEMA:
            failures.append(f"{package.name}: schema {record.get('schema')!r} != {EXPECTED_SCHEMA!r}")
            continue
        listed = {entry["path"] for entry in record.get("files", [])}
        for entry in record.get("files", []):
            target = package / entry["path"]
            if not target.is_file():
                failures.append(f"{target}: listed but missing")
                continue
            actual = sha256_file(target)
            if actual != entry["sha256"]:
                failures.append(f"{target}: sha256 {actual} != recorded {entry['sha256']}")
            checked += 1
        for present in sorted(package.rglob("*")):
            if not present.is_file():
                continue
            rel = present.relative_to(package).as_posix()
            if rel in ("PROVENANCE.yaml", "CMakeLists.txt") or rel.startswith("patches/"):
                continue
            if rel not in listed:
                failures.append(f"{present}: present but absent from PROVENANCE.yaml")
    if failures:
        for failure in failures:
            print(f"[FAIL] third-party-verify: {failure}")
        # B7b (four-element law, ADR-0060 D3): the FAIL summary teaches its
        # rule and the mechanical route; the per-finding lines above are
        # the bounded evidence.
        print("[FAIL] third-party-verify: WHY: the package tree diverged from "
              "its PROVENANCE.yaml record (rule: tpw/verify-provenance - "
              "third-party law section 7: per-file SHA-256 inventory, no "
              "unlisted files, CMakeLists per package)")
        print("       NEXT action: FIX - reconcile the listed path/digest "
              "(restore the recorded file or re-record the deliberate "
              "change through the provenance workflow), then re-run; never "
              "delete the record to pass")
        return 1
    print(f"[ OK ] third-party-verify: {len(packages)} package(s), {checked} file digest(s) verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
