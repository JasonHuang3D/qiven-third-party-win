# qiven-third-party-win

The workspace SINGLETON for third-party dependencies (Windows umbrella;
source-form packages are portable, prebuilt ones are platform-bound —
the `-win` suffix mirrors `qiven-toolchain-win`). One dependency, one
copy, one provenance record, one CMake target for the whole workspace.

Law: `qiven-devkit/docs/engineering/third-party-dependencies.md` (v2 —
workspace singleton; classes S/P/H/F; per-class CMake shapes; consumption
via the workspace adapter's identity-checked root — the workspace lock
node IS the pin, selected once). Cross-repo CMake rules:
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
- `b7b_carrier_test.py` — FAIL-carrier byte pins for the two gate legs
  (P0 four-element law; standalone suite, deliberately NOT a gate leg:
  the legs run live in every gate, the suite only pins their FAIL text).
  Run cadence: after any change to `verify_provenance.py` or
  `gate.cmd` (v61 integral-review note, 2026-10-02).

This singleton is selected ONCE in the workspace lock (a lock node;
no consumer-local SHA remains — WR-5). Consumers receive the
identity-checked root from the workspace adapter and spot-verify the
singleton HEAD against the LOCKED node commit in their own gates,
failing closed on mismatch (defense in depth).
