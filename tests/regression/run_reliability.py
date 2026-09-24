import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"

RUNS = 10
TEST_TARGET = "tests/regression/test_ai_regression.py"


def run_once(run_number):
    start = time.perf_counter()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            TEST_TARGET,
            "-q",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    elapsed = time.perf_counter() - start

    passed = result.returncode == 0

    return {
        "run": run_number,
        "status": "PASS" if passed else "FAIL",
        "return_code": result.returncode,
        "duration_seconds": round(elapsed, 4),
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    results = []

    for run_number in range(1, RUNS + 1):
        print(f"\n=== RELIABILITY RUN {run_number}/{RUNS} ===")

        result = run_once(run_number)
        results.append(result)

        print(f"Status: {result['status']}")
        print(f"Duration: {result['duration_seconds']:.2f}s")

        if result["status"] == "FAIL":
            print(result["stdout"])
            print(result["stderr"])

    passed_runs = sum(
        result["status"] == "PASS"
        for result in results
    )

    failed_runs = RUNS - passed_runs

    # A run that fails once but passes on other executions
    # is classified as a flaky run.
    flaky = failed_runs > 0 and passed_runs > 0

    pass_rate = passed_runs / RUNS
    failure_rate = failed_runs / RUNS
    flaky_rate = failure_rate if flaky else 0.0

    average_duration = (
        sum(result["duration_seconds"] for result in results)
        / RUNS
    )

    report = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "test_suite": TEST_TARGET,
        "total_runs": RUNS,
        "passed_runs": passed_runs,
        "failed_runs": failed_runs,
        "pass_rate": round(pass_rate, 4),
        "failure_rate": round(failure_rate, 4),
        "flaky": flaky,
        "flaky_rate": round(flaky_rate, 4),
        "retry_rate": 0.0,
        "average_execution_time_seconds": round(
            average_duration,
            4,
        ),
        "runs": results,
    }

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (
        REPORTS_DIR / "reliability_results.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n=== RELIABILITY SUMMARY ===")
    print(f"Total runs: {RUNS}")
    print(f"Passed: {passed_runs}")
    print(f"Failed: {failed_runs}")
    print(f"Pass rate: {pass_rate:.2%}")
    print(f"Failure rate: {failure_rate:.2%}")
    print(f"Flaky: {flaky}")
    print(f"Flaky rate: {flaky_rate:.2%}")
    print("Retry rate: 0.00%")
    print(
        f"Average execution time: "
        f"{average_duration:.2f}s"
    )
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()