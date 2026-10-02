@echo off
rem Configure every package CMakeLists standalone (root add_subdirectory).
rem B7b (four-element law): the FAIL carrier teaches its rule, keeps the
rem full cmake error as evidence (the unredirected rerun), and names the route.
setlocal
cd /d "%~dp0.."
cmake -S . -B build/smoke -G "Visual Studio 17 2022" -A x64 >nul 2>&1 || (
  echo [FAIL] configure-smoke: rerun without redirect to see the error
  echo   WHY: the root CMakeLists must configure standalone - a package
  echo   CMakeLists that only configures from inside the root is a packaging
  echo   defect ^(rule: tpw/configure-smoke^).
  echo   NEXT action: DIAGNOSE - the unredirected rerun above prints the full
  echo   cmake error; fix the named package CMakeLists, then re-run
  echo   tools\gate.cmd. Never delete the smoke to pass.
  cmake -S . -B build/smoke -G "Visual Studio 17 2022" -A x64
  exit /b 1
)
echo [ OK ] configure-smoke
exit /b 0
