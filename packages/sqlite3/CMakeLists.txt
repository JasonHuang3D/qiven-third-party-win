# packages/sqlite3 — SQLite 3 amalgamation, class S (source-compiled).
# Law: qiven-devkit docs/engineering/third-party-dependencies.md v2 (section 4.1).
# This file is the ONLY definition of qiven::tp::sqlite3; flag adaptation is
# scoped to this target and never leaks into consumers.
add_library(qiven-tp-sqlite3 STATIC src/sqlite3.c)
set_target_properties(qiven-tp-sqlite3 PROPERTIES LINKER_LANGUAGE C
    DISABLE_PRECOMPILE_HEADERS ON FOLDER "ThirdParty")
add_library(qiven::tp::sqlite3 ALIAS qiven-tp-sqlite3)

# Public headers live in src/ for this package (amalgamation layout);
# consumers #include <sqlite3.h> against this directory.
target_include_directories(qiven-tp-sqlite3 PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>)

# Upstream amalgamation: C, relaxed warnings, CRT deprecation silenced —
# all PRIVATE, on this target only.
if(MSVC)
    target_compile_options(qiven-tp-sqlite3 PRIVATE /W3 /utf-8)
else()
    target_compile_options(qiven-tp-sqlite3 PRIVATE -W3)
endif()
target_compile_definitions(
    qiven-tp-sqlite3
    PRIVATE
        _CRT_SECURE_NO_WARNINGS
        SQLITE_THREADSAFE=1 # serialized mode; single-writer discipline keeps it cheap
        SQLITE_OMIT_LOAD_EXTENSION # no dynamic extension loading from a governed host
        SQLITE_OMIT_DEPRECATED
        SQLITE_DEFAULT_FOREIGN_KEYS=0 # runtime enables per-connection (design 7.1)
        SQLITE_DEFAULT_WAL_SYNCHRONOUS=1 # FULL (design 7.1 configuration law)
        SQLITE_USE_ALLOCA=0
)

target_link_libraries(qiven-tp-sqlite3 PUBLIC advapi32)
