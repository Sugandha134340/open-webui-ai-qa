import json
import sys
from pathlib import Path


DEFAULT_THRESHOLD = 0.10


def load_pass_rate(path):
    with open(path, "r", encoding="utf-8") as f:
        report = json.load(f)

    summary = report.get("summary", {})
    return float(summary["pass_rate"])


def check_quality_drift(
    baseline_path,
    current_path,
    max_drop=DEFAULT_THRESHOLD,
):
    baseline = load_pass_rate(baseline_path)
    current = load_pass_rate(current_path)

    drop = baseline - current

    result = {
        "baseline_pass_rate": baseline,
        "current_pass_rate": current,
        "absolute_drop": max(drop, 0.0),
        "threshold": max_drop,
        "drift_detected": drop > max_drop,
    }

    return result


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python quality_drift.py "
            "<baseline_report> <current_report>"
        )
        return 2

    baseline_path = Path(sys.argv[1])
    current_path = Path(sys.argv[2])

    result = check_quality_drift(
        baseline_path,
        current_path,
    )

    print(json.dumps(result, indent=2))

    if result["drift_detected"]:
        print("QUALITY DRIFT ALERT: pass rate dropped beyond threshold.")
        return 1

    print("QUALITY DRIFT CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())