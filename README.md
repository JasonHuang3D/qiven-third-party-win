# qiven-third-party-win

The workspace SINGLETON for third-party dependencies (Windows umbrella;
source-form packages are portable, prebuilt ones are platform-bound —
the `-win` suffix mirrors `qiven-toolchain-win`). One dependency, one
copy, one provenance record, one CMake target for the whole workspace.

Law: `qiven-devkit/docs/engineering/third-party-dependencies.md` (v2 —
workspace singleton; classes S/P/H/F; per-class CMake shapes; consumption
via `QIVEN_THIRD_PARTY_ROOT` + exact-SHA pins). Cross-repo CMake rules:
`qiven-devkit/docs/conventions/cross-repo-cmake.md`.

## Packages

| Package | Class | Version | Consumers |
| --- | --- | --- | --- |
| sqlite3 | S (source-compiled) | 3.53.4 | qiven-runtime (journal subsystem, design slot TP-1) |

## Gates (tools/)

- `verify_provenance.py` — every package: digest inventory, no unlisted
  files, CMakeLists present.
- `configure-smoke.cmd` — the root CMakeLists (and therefore every
  package CMakeLists) configures standalone.
- `gate.cmd` — both, in order (the repository's local gate).

Consumers pin this repository at an exact SHA
(`QIVEN_THIRD_PARTY_PIN`, validated at their configure) and
spot-verify provenance in their own gates (defense in depth).
