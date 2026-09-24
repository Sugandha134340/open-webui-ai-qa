import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from framework.clients.ollama_client import OllamaClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"


def run_request(request_id):
    client = OllamaClient(
        model="llama3.2:3b",
        timeout=120,
    )

    start = time.perf_counter()

    try:
        result = client.generate(
            prompt=(
                f"Concurrency QA request {request_id}. "
                "Respond with a short sentence confirming the request."
            ),
            temperature=0.0,
        )

        elapsed = time.perf_counter() - start

        return {
            "request_id": request_id,
            "status": "PASS",
            "response_non_empty": bool(
                result["response"].strip()
            ),
            "latency_seconds": round(elapsed, 4),
        }

    except Exception as exc:
        elapsed = time.perf_counter() - start

        return {
            "request_id": request_id,
            "status": "ERROR",
            "response_non_empty": False,
            "latency_seconds": round(elapsed, 4),
            "error": str(exc),
        }


def test_concurrent_ollama_requests():
    """
    Concurrency invariant:
    Every submitted request must complete successfully
    and return a non-empty response.
    """

    request_count = 5

    start = time.perf_counter()

    results = []

    with ThreadPoolExecutor(
        max_workers=request_count
    ) as executor:

        futures = [
            executor.submit(
                run_request,
                request_id,
            )
            for request_id in range(1, request_count + 1)
        ]

        for future in as_completed(futures):
            results.append(
                future.result()
            )

    wall_clock = time.perf_counter() - start

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
        and result["response_non_empty"]
    )

    errors = [
        result
        for result in results
        if result["status"] == "ERROR"
    ]

    report = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "test_type": "concurrency",
        "model": "llama3.2:3b",
        "concurrent_requests": request_count,
        "wall_clock_seconds": round(
            wall_clock,
            4,
        ),
        "successful_requests": passed,
        "failed_requests": len(errors),
        "error_rate": round(
            len(errors) / request_count,
            4,
        ),
        "results": sorted(
            results,
            key=lambda item: item["request_id"],
        ),
    }

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (
        REPORTS_DIR /
        "concurrency_results.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n=== CONCURRENCY TEST ===")
    print(
        f"Concurrent requests: {request_count}"
    )
    print(
        f"Successful: {passed}"
    )
    print(
        f"Failed: {len(errors)}"
    )
    print(
        f"Error rate: "
        f"{report['error_rate']:.2%}"
    )
    print(
        f"Wall-clock time: "
        f"{wall_clock:.2f}s"
    )
    print(
        f"Report: {report_path}"
    )

    assert len(results) == request_count
    assert passed == request_count
    assert len(errors) == 0