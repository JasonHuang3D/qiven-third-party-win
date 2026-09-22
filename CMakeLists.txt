cmake_minimum_required(VERSION 3.24)

# Singleton configure-smoke root: every package CMakeLists must CONFIGURE
# standalone from this tree (gate task configure-smoke). Not a product
# build system; consumers add the packages they use from their own trees
# (Devkit conventions: cross-repo-cmake.md; standard section 5).
project(qiven-third-party-win VERSION 0.1.0 LANGUAGES C CXX)

add_subdirectory(packages/sqlite3)
