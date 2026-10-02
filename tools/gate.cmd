@echo off
rem Singleton local gate: provenance verify + configure smoke (README law).
rem B7b (four-element law): a failing leg names its class and route before
rem the gate fails; the relayed tool output above is the evidence.
setlocal
cd /d "%~dp0.."
echo [ RUN] verify-provenance
python tools\verify_provenance.py || (
  echo [FAIL] gate:local FAIL - leg 1/2 verify-provenance
  echo   NEXT action: FIX - the [FAIL] rows above name each provenance
  echo   divergence; reconcile the record, then re-run tools\gate.cmd.
  exit /b 1
)
echo [ RUN] configure-smoke
call tools\configure-smoke.cmd || (
  echo [FAIL] gate:local FAIL - leg 2/2 configure-smoke
  echo   NEXT action: DIAGNOSE - the configure-smoke FAIL block above carries
  echo   the full cmake error on its unredirected rerun; fix the named
  echo   package CMakeLists, then re-run tools\gate.cmd.
  exit /b 1
)
echo [ OK ] gate:local PASS
exit /b 0
