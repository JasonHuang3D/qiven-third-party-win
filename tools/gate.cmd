@echo off
rem Singleton local gate: provenance verify + configure smoke (README law).
setlocal
cd /d "%~dp0.."
echo [ RUN] verify-provenance
python tools\verify_provenance.py || exit /b 1
echo [ RUN] configure-smoke
call tools\configure-smoke.cmd || exit /b 1
echo [ OK ] gate:local PASS
exit /b 0
