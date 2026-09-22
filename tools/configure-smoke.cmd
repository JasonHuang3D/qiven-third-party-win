@echo off
rem Configure every package CMakeLists standalone (root add_subdirectory).
setlocal
cd /d "%~dp0.."
cmake -S . -B build/smoke -G "Visual Studio 17 2022" -A x64 >nul 2>&1 || (
  echo [FAIL] configure-smoke: rerun without redirect to see the error
  cmake -S . -B build/smoke -G "Visual Studio 17 2022" -A x64
  exit /b 1
)
echo [ OK ] configure-smoke
exit /b 0
