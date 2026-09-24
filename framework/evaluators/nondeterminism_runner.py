import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from framework.clients.ollama_client import OllamaClient
from framework.evaluators.dataset_loader import load_ai_scenarios


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"

REPETITIONS = 10

SCENARIO_IDS = [
    "AI026",
    "AI027",
    "AI028",
]


def normalize(text):
    return " ".join(text.lower().split())


def evaluate_response(scenario_id, response):
    text = normalize(response)

    if scenario_id == "AI026":
        return "paris" in text

    if scenario_id == "AI027":
        return "136" in text

    if scenario_id == "AI028":
        required_concepts = [
            "left",
            "right",
            "less",
            "greater",
        ]

        return all(
            concept in text
            for concept in required_concepts
        )

    return False


def build_prompt(scenario):
    context = scenario.get("context", "")
    user_input = scenario.get("input", "")
    constraints = scenario.get("constraints", [])

    constraints_text = "\n".join(
        f"- {constraint}"
        for constraint in constraints
    )

    return f"""
Context:
{context}

User request:
{user_input}

Constraints:
{constraints_text}

Answer the user's request directly.
Follow the provided constraints.
Do not invent information or sources.
""".strip()


def main():
    scenarios = load_ai_scenarios()

    scenario_map = {
        scenario["scenario_id"]: scenario
        for scenario in scenarios
    }

    client = OllamaClient(
        model="llama3.2:3b",
        timeout=120,
    )

    all_results = []

    for scenario_id in SCENARIO_IDS:

        scenario = scenario_map[scenario_id]
        prompt = build_prompt(scenario)

        print(
            f"\n=== {scenario_id}: "
            f"{REPETITIONS} repetitions ==="
        )

        scenario_results = []

        for run_number in range(1, REPETITIONS + 1):

            start = time.perf_counter()

            try:
                result = client.generate(
                    prompt=prompt,
                    temperature=0.0,
                )

                response = result["response"]

                passed = evaluate_response(
                    scenario_id,
                    response,
                )

                latency = result[
                    "latency_seconds"
                ]

                status = (
                    "PASS"
                    if passed
                    else "FAIL"
                )

                print(
                    f"Run {run_number:02d}: "
                    f"{status} | "
                    f"{latency:.2f}s"
                )

                scenario_results.append({
                    "run": run_number,
                    "status": status,
                    "response": response,
                    "latency_seconds": latency,
                })

            except Exception as exc:

                elapsed = time.perf_counter() - start

                print(
                    f"Run {run_number:02d}: "
                    f"ERROR | "
                    f"{elapsed:.2f}s"
                )

                scenario_results.append({
                    "run": run_number,
                    "status": "ERROR",
                    "error": str(exc),
                    "execution_time_seconds": round(
                        elapsed,
                        4,
                    ),
                })

        statuses = [
            result["status"]
            for result in scenario_results
        ]

        counts = Counter(statuses)

        passed_count = counts["PASS"]
        failed_count = counts["FAIL"]
        error_count = counts["ERROR"]

        pass_rate = (
            passed_count / REPETITIONS
        )

        # Tolerance model:
        # >= 80% successful executions = stable
        # 0% success = stable failure
        # otherwise = stochastic/flaky behavior
        if pass_rate >= 0.80:
            classification = "STABLE_PASS"
        elif pass_rate == 0:
            classification = "STABLE_FAIL"
        else:
            classification = "FLAKY"

        summary = {
            "scenario_id": scenario_id,
            "repetitions": REPETITIONS,
            "passed": passed_count,
            "failed": failed_count,
            "errors": error_count,
            "pass_rate": round(
                pass_rate,
                4,
            ),
            "classification": classification,
        }

        print(
            f"Summary: "
            f"{passed_count}/{REPETITIONS} passed | "
            f"{classification}"
        )

        all_results.append({
            "scenario": summary,
            "runs": scenario_results,
        })

    report = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "model": "llama3.2:3b",

        "temperature": 0.0,

        "repetitions_per_scenario": REPETITIONS,

        "tolerance_model": {
            "stable_pass": ">= 80% pass rate",
            "flaky": "1% to 79% pass rate",
            "stable_fail": "0% pass rate",
            "errors": (
                "Infrastructure/dependency failure "
                "reported separately"
            ),
        },

        "scenarios": all_results,
    }

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (
        REPORTS_DIR
        / "nondeterminism_results.json"
    )

    with report_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\nReport saved to: {report_path}"
    )


if __name__ == "__main__":
    main()