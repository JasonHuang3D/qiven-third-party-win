# qiven-third-party-win Agent Contract

The workspace singleton for third-party dependencies. Read `README.md`
first.

- Engineering conventions (naming, layout, scripts, CMake, cross-repo
  consumption) are canonical in the Devkit: `docs/conventions/README.md`
  there. The third-party law itself is
  `docs/engineering/third-party-dependencies.md` there (v2: this
  repository IS the singleton; per-repo third_party/ is forbidden).
- Every package change updates its PROVENANCE.yaml in the same commit;
  the gate verifies digests — never edit vendored files casually.
- Roles, typed handoffs, execution authority and workflow are canonical
  in `JasonHuang3D/qiven-context`. This file grants no authority and
  repeats no contracts.
