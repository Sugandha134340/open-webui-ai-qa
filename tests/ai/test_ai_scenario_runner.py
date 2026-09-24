
from framework.evaluators.ai_scenario_runner import (
    AIScenarioRunner,
)


def test_runner_initializes():
    runner = AIScenarioRunner()

    assert runner.model == "llama3.2:3b"
    assert runner.temperature == 0.0


def test_prompt_contains_scenario_information():
    runner = AIScenarioRunner()

    scenario = {
        "scenario_id": "TEST001",
        "input": "What is precision?",
        "context": "Machine learning context.",
        "constraints": [
            "Answer directly",
            "Do not invent sources",
        ],
    }

    prompt = runner.build_prompt(
        scenario
    )

    assert "What is precision?" in prompt
    assert "Machine learning context." in prompt
    assert "Answer directly" in prompt
    assert "Do not invent sources" in prompt


def test_build_report():
    runner = AIScenarioRunner()

    results = [
        {
            "scenario_id": "AI001",
            "status": "PASS",
            "latency_seconds": 2.0,
        },
        {
            "scenario_id": "AI002",
            "status": "FAIL",
            "latency_seconds": 4.0,
        },
        {
            "scenario_id": "AI003",
            "status": "ERROR",
        },
    ]

    report = runner.build_report(
        results
    )

    assert report["summary"]["total_scenarios"] == 3
    assert report["summary"]["passed"] == 1
    assert report["summary"]["failed"] == 1
    assert report["summary"]["errors"] == 1
    assert report["summary"]["evaluated"] == 2
    assert report["summary"]["pass_rate"] == 0.5
    assert report["summary"][
        "average_latency_seconds"
    ] == 3.0


def test_save_report(tmp_path):
    runner = AIScenarioRunner()

    report = runner.build_report([])

    import framework.evaluators.ai_scenario_runner as module

    original_dir = module.REPORTS_DIR

    try:
        module.REPORTS_DIR = tmp_path

        path = runner.save_report(
            report,
            "test_scenario_results.json",
        )

        assert path.exists()
        assert path.name == (
            "test_scenario_results.json"
        )

    finally:
        module.REPORTS_DIR = original_dir


import pytest

from framework.evaluators.ai_scenario_runner import (
    AIScenarioRunner,
)


@pytest.mark.integration
def test_run_all_ai_scenarios():
    runner = AIScenarioRunner(
        model="llama3.2:3b",
        temperature=0.0,
        timeout=120,
    )

    report = runner.run_all()

    report_path = runner.save_report(report)

    print("\n=== AI SCENARIO BASELINE ===")
    print(
        f"Total scenarios: "
        f"{report['summary']['total_scenarios']}"
    )
    print(
        f"Passed: "
        f"{report['summary']['passed']}"
    )
    print(
        f"Failed: "
        f"{report['summary']['failed']}"
    )
    print(
        f"Errors: "
        f"{report['summary']['errors']}"
    )
    print(
        f"Pass rate: "
        f"{report['summary']['pass_rate']:.2%}"
    )
    print(
        f"Average latency: "
        f"{report['summary']['average_latency_seconds']:.2f}s"
    )
    print(
        f"Report: {report_path}"
    )

    assert report["summary"]["total_scenarios"] == 35
    assert report["summary"]["evaluated"] > 0
    assert report["summary"]["errors"] == 0
