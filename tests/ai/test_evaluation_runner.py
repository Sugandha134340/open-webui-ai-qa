from framework.evaluators.evaluation_runner import (
    EvaluationRunner,
)


def test_runner_evaluates_provided_responses():
    runner = EvaluationRunner()

    response_map = {
        "AI001": "QA_PASS_123",
    }

    # AI001 may use a different evaluation definition
    # in the dataset, so we verify the runner structure
    # rather than assuming its exact expected response.
    report = runner.run(response_map)

    assert "summary" in report
    assert "results" in report

    assert report["summary"]["total_scenarios"] == 35


def test_runner_marks_missing_responses_as_not_run():
    runner = EvaluationRunner()

    report = runner.run({})

    summary = report["summary"]

    assert summary["total_scenarios"] == 35
    assert summary["evaluated"] == 0
    assert summary["not_run"] == 35
    assert summary["passed"] == 0
    assert summary["failed"] == 0


def test_runner_evaluates_exact_match_response():
    runner = EvaluationRunner()

    scenario = {
        "scenario_id": "TEST001",
        "category": "normal",
        "severity": "low",
        "evaluation_type": "exact_match",
        "expected_answer": "QA_PASS",
    }

    result = runner.evaluate_response(
        scenario,
        "QA_PASS",
    )

    assert result["scenario_id"] == "TEST001"
    assert result["result"]["passed"] is True
    assert result["result"]["score"] == 1.0


def test_runner_detects_exact_match_failure():
    runner = EvaluationRunner()

    scenario = {
        "scenario_id": "TEST002",
        "category": "normal",
        "severity": "medium",
        "evaluation_type": "exact_match",
        "expected_answer": "QA_PASS",
    }

    result = runner.evaluate_response(
        scenario,
        "WRONG",
    )

    assert result["scenario_id"] == "TEST002"
    assert result["result"]["passed"] is False
    assert result["result"]["score"] == 0.0


def test_runner_saves_report(tmp_path):
    runner = EvaluationRunner()

    report = runner.run({})

    # Temporarily redirect the report directory
    # for this test.
    import framework.evaluators.evaluation_runner as runner_module

    original_reports_dir = runner_module.REPORTS_DIR

    try:
        runner_module.REPORTS_DIR = tmp_path

        report_path = runner.save_report(
            report,
            "test_ai_report.json",
        )

        assert report_path.exists()
        assert report_path.name == "test_ai_report.json"

    finally:
        runner_module.REPORTS_DIR = original_reports_dir


def test_golden_regression_loads_all_cases():
    runner = EvaluationRunner()

    report = runner.run_golden_regression({})

    assert report["type"] == "golden_regression"
    assert report["total_cases"] == 10
    assert report["passed"] == 0
    assert report["failed"] == 0
    assert report["not_run"] == 10
    assert report["regression_detected"] is False


def test_golden_regression_detects_failure():
    runner = EvaluationRunner()

    # Deliberately provide an incorrect response for
    # one golden case.
    response_map = {
        "AI001": "password = secret123"
    }

    report = runner.run_golden_regression(
        response_map
    )

    ai001 = next(
        result
        for result in report["results"]
        if result["scenario_id"] == "AI001"
    )

    assert ai001["status"] == "FAIL"
    assert report["failed"] >= 1
    assert report["regression_detected"] is True

