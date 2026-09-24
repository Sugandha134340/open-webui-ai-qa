import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from framework.clients.ollama_client import OllamaClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"

CONCURRENCY_LEVELS = [1, 3, 5]


def percentile(values, percentile):
    if not values:
        return 0.0

    values = sorted(values)

    index = (
        (len(values) - 1)
        * percentile
        / 100
    )

    lower = int(index)
    upper = min(
        lower + 1,
        len(values) - 1,
    )

    fraction = index - lower

    return (
        values[lower]
        + (
            values[upper]
            - values[lower]
        )
        * fraction
    )


def run_request(request_id):
    client = OllamaClient(
        model="llama3.2:3b",
        timeout=120,
    )

    start = time.perf_counter()

    try:
        result = client.generate(
            prompt=(
                f"Performance QA request {request_id}. "
                "Reply with one short sentence."
            ),
            temperature=0.0,
        )

        elapsed = time.perf_counter() - start

        return {
            "request_id": request_id,
            "status": "PASS",
            "latency_seconds": round(
                elapsed,
                4,
            ),
            "response_non_empty": bool(
                result["response"].strip()
            ),
        }

    except Exception as exc:
        elapsed = time.perf_counter() - start

        return {
            "request_id": request_id,
            "status": "ERROR",
            "latency_seconds": round(
                elapsed,
                4,
            ),
            "response_non_empty": False,
            "error": str(exc),
        }


def run_level(concurrency):
    start = time.perf_counter()

    results = []

    with ThreadPoolExecutor(
        max_workers=concurrency
    ) as executor:

        futures = [
            executor.submit(
                run_request,
                request_id,
            )
            for request_id in range(
                1,
                concurrency + 1,
            )
        ]

        for future in as_completed(futures):
            results.append(
                future.result()
            )

    wall_clock = (
        time.perf_counter() - start
    )

    successful = [
        result
        for result in results
        if result["status"] == "PASS"
        and result["response_non_empty"]
    ]

    errors = [
        result
        for result in results
        if result["status"] == "ERROR"
    ]

    latencies = [
        result["latency_seconds"]
        for result in successful
    ]

    return {
        "concurrency": concurrency,
        "requests": len(results),
        "successful": len(successful),
        "failed": len(errors),
        "error_rate": round(
            len(errors) / len(results),
            4,
        ),
        "wall_clock_seconds": round(
            wall_clock,
            4,
        ),
        "average_latency_seconds": round(
            statistics.mean(latencies),
            4,
        ) if latencies else 0.0,
        "p50_latency_seconds": round(
            percentile(latencies, 50),
            4,
        ),
        "p95_latency_seconds": round(
            percentile(latencies, 95),
            4,
        ),
        "results": results,
    }


def test_ollama_load_levels():
    """
    Measure latency and error behavior at increasing
    concurrency levels.
    """

    levels = []

    for concurrency in CONCURRENCY_LEVELS:
        print(
            f"\n=== CONCURRENCY {concurrency} ==="
        )

        result = run_level(
            concurrency
        )

        levels.append(result)

        print(
            f"Successful: "
            f"{result['successful']}/"
            f"{result['requests']}"
        )

        print(
            f"Error rate: "
            f"{result['error_rate']:.2%}"
        )

        print(
            f"Wall-clock: "
            f"{result['wall_clock_seconds']:.2f}s"
        )

        print(
            f"Average latency: "
            f"{result['average_latency_seconds']:.2f}s"
        )

        print(
            f"P50 latency: "
            f"{result['p50_latency_seconds']:.2f}s"
        )

        print(
            f"P95 latency: "
            f"{result['p95_latency_seconds']:.2f}s"
        )

    report = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "test_type": "stepped_load",
        "model": "llama3.2:3b",
        "concurrency_levels": CONCURRENCY_LEVELS,
        "levels": levels,
    }

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (
        REPORTS_DIR /
        "performance_results.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"\nReport: {report_path}"
    )

    assert all(
        level["failed"] == 0
        for level in levels
    )