# packages/sqlite3 — SQLite 3 amalgamation (class S, source-compiled)

- Class **S** (pristine upstream source) per the Devkit standard
  `docs/engineering/third-party-dependencies.md` v2; version 3.53.4.
- Target: `qiven::tp::sqlite3` (this package's CMakeLists is the only
  definition). Compile-flag adaptation is scoped to the target.
- Consumers: qiven-runtime journal subsystem (design slot TP-1,
  runtime-production-mvp-cpp-design.md section 7/17).
- Upstream archive digest at acquisition: SHA3-256
  628a44cfe82c66aed1ccbbe85a562d2e33ebe64b3288981ed76285612227934e
  (sqlite.org download page, 2026-09-23).
- License: Public Domain (LICENSE; sqlite.org/copyright.html).
- Patches: none (pristine).
