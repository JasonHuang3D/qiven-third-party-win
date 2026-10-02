from __future__ import annotations

"""B7b carrier fixture suite (ADR-0060 D3; P0 repair batch B7b, 2026-10-02).

Pins the four-element FAIL carriers of this repository's singleton gate
surface (register rows thirdpartywin-gate-cmd,
thirdpartywin-verify-provenance, thirdpartywin-configure-smoke):

  B7b-T1  verify_provenance digest-mismatch FAIL teaches rule + FIX
          route (behavioral: temp singleton tree via the module ROOT
          seam; run standalone - the README law defines gate.cmd as the
          two-leg verify+configure gate, this suite is the diagnostic
          carrier proof, not a gate leg)
  B7b-T2  configure-smoke.cmd FAIL block carries WHY + DIAGNOSE route
          while keeping the unredirected-rerun evidence mechanism
          (source pin; cmake configure is the gate leg's own job)
  B7b-T3  gate.cmd failing legs name the failing leg and its route
          before exit 1; PASS selectors stay byte-stable (source pin)

Disposable temp fixtures only (testing law: tests never touch the
developer's repository). Each case id rides in the failure message.
"""

import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_provenance as vp  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CHECKS = 0


def check(condition: bool, label: str, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(f"[{label}] {detail}" if detail else f"[{label}] assertion failed")


def case_t1() -> None:
    with tempfile.TemporaryDirectory(prefix="tpw-b7b-") as tmp:
        root = Path(tmp)
        package = root / "packages" / "demo"
        package.mkdir(parents=True)
        (package / "PROVENANCE.yaml").write_text(
            "schema: qiven-third-party-provenance-v2\n"
            "files:\n"
            "  - path: payload.txt\n"
            "    sha256: 0000000000000000000000000000000000000000000000000000000000000000\n",
            encoding="utf-8")
        (package / "CMakeLists.txt").write_text("# stub\n", encoding="utf-8")
        (package / "payload.txt").write_text("live bytes\n", encoding="utf-8")
        real_root, real_packages = vp.ROOT, vp.PACKAGES
        captured = io.StringIO()
        try:
            vp.ROOT = root
            vp.PACKAGES = root / "packages"
            with contextlib.redirect_stdout(captured):
                code = vp.main()
        finally:
            vp.ROOT, vp.PACKAGES = real_root, real_packages
        text = captured.getvalue()
        check(code == 1, "B7b-T1", f"expected exit 1, got {code}: {text}")
        check("sha256" in text and "payload.txt" in text, "B7b-T1",
              "digest finding listed: " + text)
        check("[FAIL] third-party-verify: WHY:" in text, "B7b-T1", "WHY present")
        check("rule: tpw/verify-provenance" in text, "B7b-T1", "rule present")
        check("NEXT action: FIX - reconcile the listed path/digest" in text,
              "B7b-T1", "FIX route present")
        check("never delete the record to pass" in text, "B7b-T1",
              "anti-weakening law")


def case_t2() -> None:
    text = (ROOT / "tools" / "configure-smoke.cmd").read_text(encoding="utf-8")
    check("rerun without redirect to see the error" in text, "B7b-T2",
          "pinned evidence mechanism kept")
    check("WHY: the root CMakeLists must configure standalone" in text, "B7b-T2",
          "WHY present")
    check("rule: tpw/configure-smoke" in text, "B7b-T2", "rule token")
    check("NEXT action: DIAGNOSE - the unredirected rerun above" in text,
          "B7b-T2", "DIAGNOSE route")
    check("Never delete the smoke to pass." in text, "B7b-T2",
          "anti-weakening law")
    check("echo [ OK ] configure-smoke" in text, "B7b-T2", "PASS selector kept")


def case_t3() -> None:
    text = (ROOT / "tools" / "gate.cmd").read_text(encoding="utf-8")
    check("[FAIL] gate:local FAIL - leg 1/2 verify-provenance" in text, "B7b-T3",
          "leg-1 failure class")
    check("[FAIL] gate:local FAIL - leg 2/2 configure-smoke" in text, "B7b-T3",
          "leg-2 failure class")
    check("NEXT action: FIX - the [FAIL] rows above name each provenance"
          in text, "B7b-T3", "leg-1 route")
    check("NEXT action: DIAGNOSE - the configure-smoke FAIL block above"
          in text, "B7b-T3", "leg-2 route")
    check("echo [ RUN] verify-provenance" in text, "B7b-T3", "RUN selector kept")
    check("echo [ OK ] gate:local PASS" in text, "B7b-T3", "PASS selector kept")


def main() -> int:
    case_t1()
    case_t2()
    case_t3()
    print(f"[ OK ] tpw B7b carrier fixtures ({CHECKS} checks)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as failure:
        print(f"[FAIL] b7b-carrier-tests: {failure}", file=sys.stderr)
        print("[FAIL] b7b-carrier-tests: WHY: a pinned four-element carrier "
              "selector broke (rule: tpw/b7b-carriers)", file=sys.stderr)
        print("       NEXT action: FIX - the B7b-Tn id above names the carrier; "
              "restore the four-element law, never the check", file=sys.stderr)
        raise SystemExit(1)
