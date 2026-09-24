# Test Strategy

## 1. Purpose

This document defines the QA strategy for Open WebUI v0.11.4.

The strategy focuses on building reusable, evidence-driven automation that validates not only whether the application works, but also whether AI behavior remains correct, safe, consistent, reliable, and diagnosable.

The strategy covers:

- UI automation
- API/backend testing
- end-to-end workflows
- integration and dependency failures
- AI/LLM evaluation
- non-deterministic behavior
- golden regression testing
- safety and adversarial testing
- reliability and flakiness
- concurrency
- performance
- CI/CD quality gates
- root-cause analysis
- security/privacy-aware QA
- diagnostic evidence

---

## 2. Testing Principles

### 2.1 Risk-Based Testing

Testing effort is concentrated on areas with the greatest impact on AI application quality:

1. AI evaluation correctness
2. Reusable automation architecture
3. Critical workflows
4. Reliability and flakiness
5. CI/CD quality gates
6. Performance
7. Root-cause analysis

The project prioritizes meaningful coverage rather than maximizing the number of shallow tests.

---

### 2.2 Evidence-Driven Testing

Every important failure should produce enough evidence to determine:

```text
What failed?
    ↓
Where did it fail?
    ↓
Can it be reproduced?
    ↓
What evidence supports the finding?
    ↓
Is it a product issue, AI variance,
test issue, infrastructure issue, or environment limitation?
```

Evidence includes, where applicable:

- test output
- API responses
- AI evaluation results
- latency measurements
- screenshots
- browser information
- error messages
- execution duration
- CI results
- repeated-run results

---

### 2.3 Layered Testing

The framework uses multiple testing layers instead of depending on a single end-to-end suite.

```text
                    Test Strategy
                         |
       +-----------------+-----------------+
       |                 |                 |
       v                 v                 v
      UI               API              AI/LLM
       |                 |                 |
       +-----------------+-----------------+
                         |
                    Integration
                         |
             +-----------+-----------+
             |                       |
             v                       v
        Dependency              Performance
        / Failure                  /
        Injection               Concurrency
```

This allows failures to be isolated closer to the component where they occur.

---

## 3. Test Levels

### 3.1 UI Testing

Browser automation validates observable frontend behavior.

Coverage includes:

- application loading
- authentication redirect
- login-page discovery
- chat-page routing
- browser-specific behavior

Browsers currently covered:

```text
Chromium
Firefox
```

Playwright is used for browser automation.

---

### 3.2 API and Backend Testing

API testing validates:

- endpoint availability
- authentication behavior
- authorization
- invalid credentials
- protected endpoints
- application version
- backend integration

API tests are implemented using Python/pytest and HTTP requests.

---

### 3.3 Integration Testing

Integration tests verify communication with the local Ollama backend.

Coverage includes:

- connectivity
- health
- model availability
- generation
- dependency failure handling

Dependency failures are simulated without requiring the actual external dependency to be broken.

---

### 3.4 AI Evaluation Testing

AI evaluation is treated as a separate testing layer.

The framework evaluates observable AI responses using:

- rule-based evaluation
- semantic evaluation
- structured validation
- safety checks
- exact-match checks where appropriate
- arithmetic validation
- consistency checks
- contextual evaluation

The framework does not attempt to evaluate hidden chain-of-thought.

---

## 4. AI Evaluation Strategy

### 4.1 Scenario Dataset

A structured dataset containing **35 AI scenarios** is used.

The dataset covers:

```text
Normal requests
Edge cases
Ambiguous requests
Contradictory instructions
Out-of-scope requests
Prompt injection
Safety
Groundedness
Consistency
Multi-turn behavior
Long input
Instruction following
Hallucination
Robustness
```

Each scenario contains structured information such as:

- scenario ID
- category
- input
- context
- expected behavior
- constraints
- safety requirement
- evaluation method
- severity

---

### 4.2 Evaluation Dimensions

The framework evaluates applicable AI-quality dimensions including:

- correctness
- relevance
- consistency
- groundedness
- safety
- constraint adherence
- failure handling
- latency
- instruction following

For applicable scenarios, the framework uses deterministic checks in addition to semantic evaluation.

---

### 4.3 Rule-Based Evaluation

Rule-based checks are used where deterministic validation is appropriate.

Examples include:

```text
Exact output
Required terms
Word count
Bullet count
Refusal detection
Secret-like content detection
Arithmetic correctness
```

Deterministic checks reduce unnecessary dependence on a semantic judge.

---

### 4.4 Semantic Evaluation

A local Ollama model is used as a semantic evaluator for scenarios where exact string matching is inappropriate.

The evaluator assesses whether the generated response satisfies scenario-specific requirements.

The semantic judge returns structured evaluation information including:

```text
Pass/fail
Score
Individual criteria
Reason
```

---

## 5. Non-Deterministic Evaluation Strategy

AI output is not assumed to be identical across executions.

Important scenarios are therefore evaluated repeatedly.

The project uses:

```text
10 repetitions per selected nondeterminism scenario
```

The current nondeterminism evaluation covers three scenarios with:

```text
30 total executions
30 stable passes
0 errors
```

The framework distinguishes:

```text
Expected AI variance
        ≠
AI quality regression
        ≠
Evaluator variance
        ≠
Infrastructure failure
```

---

## 6. Tolerance Model

The project does not treat a single AI execution as definitive for stochastic behavior.

The following principles are used:

### Stable Pass

A scenario consistently satisfies the expected behavior across repeated executions.

### Stable Failure

A scenario consistently violates the expected behavior.

### Stochastic / AI Variance

The model produces different outcomes across executions and the difference is attributable to probabilistic behavior rather than an application or evaluator defect.

### Evaluator Variance

The response remains correct or unchanged, but the evaluation system produces inconsistent judgments.

### Infrastructure Failure

The evaluation cannot complete because of an unavailable dependency, timeout, service failure, or equivalent runtime problem.

### Quality Problem

Variance becomes a quality concern when repeated execution causes meaningful degradation in task success, safety, correctness, or another explicitly measured requirement.

---

## 7. Golden Regression Strategy

A golden dataset is used to detect important AI-quality regressions.

The regression suite covers:

- precision/recall explanation
- arithmetic correctness
- exact output requirements

The framework also includes deliberate incorrect outputs to verify that regressions are actually detected.

The regression suite therefore tests both:

```text
Correct behavior → accepted
Incorrect behavior → rejected
```

---

## 8. Judge Validation Strategy

Because an LLM-based semantic judge is used, it is validated against a human-labeled dataset.

Validation dataset:

```text
12 cases
```

Observed result:

```text
Correct judgments: 10
False positives: 2
False negatives: 0
Validation rate: 83.33%
```

The result is treated as evidence about the implemented judge on the validation dataset rather than as a universal measure of judge accuracy.

Known judge limitations are documented in the AI evaluation results and RCA.

---

## 9. Safety and Adversarial Testing Strategy

Safety scenarios are evaluated separately from ordinary AI-quality scenarios.

Coverage includes:

- prompt injection
- instruction override
- system/developer instruction extraction
- fake system messages
- sensitive-information requests
- secret exposure
- credential bypass
- phishing
- dangerous requests
- out-of-scope requests

The framework records safety results separately so that safety failures are not hidden inside an overall quality average.

---

## 10. Dependency Failure Strategy

Dependency failures are deliberately simulated to verify safe failure behavior.

The test suite covers:

```text
HTTP 500
Timeout
Malformed response
Empty response
Unavailable dependency
HTTP 429 / rate limiting
Partial response
```

The expected behavior is that the framework detects the failure and does not incorrectly treat the response as a successful AI result.

Current dependency test result:

```text
7 tests
7 passed
```

---

## 11. Reliability and Flakiness Strategy

The important regression suite is executed repeatedly without automatic retries hiding failures.

The reliability runner performs:

```text
10 complete suite executions
```

and records:

- pass/failure
- return code
- execution time
- stdout
- stderr
- retry count

Observed result:

```text
10 runs
7 passed
3 failed
70% suite pass rate
30% suite failure rate
0 retries
~15.89s average runtime
```

The three failures were associated with AI001.

Additional evaluation showed that the same AI001 response could receive a passing semantic/rule-based evaluation, supporting the classification as evaluator/judge variance rather than a demonstrated regression in the golden response.

---

## 12. Concurrency Strategy

Concurrent AI requests are used to validate parallel request handling.

The test submits:

```text
5 simultaneous requests
```

and verifies that each request produces a valid response.

Expected invariant:

```text
Every submitted request should complete
without an unexpected request failure.
```

Observed result:

```text
5/5 successful
0 failures
```

---

## 13. Performance Strategy

Performance testing evaluates an AI path at increasing concurrency levels:

```text
1
3
5
10
```

The following measurements are collected:

- average latency
- P50 latency
- P95 latency
- wall-clock duration
- error rate
- concurrency
- resource samples

Latest observed results:

| Concurrency | Average | P50 | P95 | Error Rate |
|---:|---:|---:|---:|---:|
| 1 | 10.77s | 10.77s | 10.77s | 0% |
| 3 | 4.31s | 4.32s | 5.42s | 0% |
| 5 | 5.13s | 4.97s | 7.16s | 0% |
| 10 | 8.10s | 8.30s | 12.46s | 0% |

The tested configuration showed increased latency at higher concurrency.

No breaking point was observed within the tested range of 1–10 concurrent requests.

---

## 14. Resource Monitoring Strategy

Docker resource telemetry is sampled during performance execution.

The current implementation records resource information for the:

```text
open-webui
```

container.

Because the AI benchmark sends requests directly to Ollama, this telemetry does not represent complete resource consumption of the Ollama/model process.

GPU and host-level resource telemetry are not currently captured.

This is documented as a coverage limitation rather than presented as complete resource monitoring.

---

## 15. Security and Privacy Strategy

Security testing is focused on quality validation rather than penetration testing.

The strategy covers relevant behaviors such as:

- unauthorized access
- protected endpoints
- invalid authentication
- sensitive-information requests
- secret exposure
- credential bypass
- phishing
- potential cross-user access concerns

Some authenticated security workflows could not be completed because valid QA credentials were unavailable.

---

## 16. Persistence and Recovery Strategy

The application uses a persistent Docker volume mounted at:

```text
/app/backend/data
```

The strategy validates:

```text
Container running
      ↓
Persistent volume present
      ↓
Container restart
      ↓
Healthy state
      ↓
Application API available
```

After restart:

```text
Container: healthy
/api/version: HTTP 200
Version: 0.11.4
```

Individual authenticated user/chat record integrity could not be directly validated because valid QA credentials were unavailable.

---

## 17. CI/CD Strategy

The framework is integrated with GitHub Actions.

The CI pipeline executes automated quality checks and contains a quality gate.

A deliberate regression was introduced into the quality-gate test to demonstrate:

```text
Code Change
    ↓
CI Execution
    ↓
Test Failure
    ↓
Quality Gate Failure
    ↓
Build Blocked
```

The regression was then reverted and the pipeline returned to the expected passing state.

This provides evidence that the CI quality gate is capable of detecting an introduced regression.

---

## 18. Observability and Diagnostic Evidence

The test framework records evidence needed to investigate failures, including where applicable:

- test results
- API responses
- AI responses
- evaluator scores
- evaluation criteria
- latency
- execution duration
- concurrency results
- browser information
- CI results
- dependency failure information
- RCA findings

The goal is diagnosability rather than building a complete production monitoring platform.

---

## 19. Root-Cause Analysis Strategy

Significant failures are investigated using a structured RCA process.

Each RCA considers:

1. Failure/scenario
2. Expected behavior
3. Actual behavior
4. Reproduction
5. Evidence
6. Severity/impact
7. Affected component
8. Root cause or classification
9. Confidence level
10. Prevention
11. Regression test

The analysis distinguishes:

```text
Observed fact
      ↓
Hypothesis
      ↓
Evidence
      ↓
Confirmed classification/root cause
```

The project contains five documented RCA cases.

---

## 20. Failure Classification Model

Failures are classified using the following categories:

| Classification | Meaning |
|---|---|
| Product regression | Application behavior changed incorrectly |
| AI/application behavior | Observable AI behavior violates an expected requirement |
| AI variance | Different valid/invalid model outputs occur across runs |
| Evaluator variance | Evaluation result changes while the underlying response remains unchanged |
| Flaky test | Test result changes without a corresponding product change |
| Infrastructure failure | Runtime/dependency/environment prevents execution |
| Environment limitation | Required test setup or credentials are unavailable |
| Test defect | The test itself incorrectly identifies expected behavior as a failure |

This classification is central to the project because a failed AI evaluation should not automatically be treated as an application regression.

---

## 21. CI Quality Gates

Critical test failures are intended to prevent a successful CI quality gate.

The quality infrastructure therefore acts as:

```text
Test
 ↓
Evaluation
 ↓
Classification
 ↓
Quality Gate
 ↓
Pass / Block
```

Non-critical observations and known environment limitations are documented separately so that they do not become misleading product-regression claims.

---

## 22. Known Testing Limitations

The current strategy has the following documented limitations:

- Positive authenticated Open WebUI workflows require valid QA credentials.
- Authenticated streaming/real-time E2E could not be fully exercised.
- Authenticated user/chat persistence could not be directly validated.
- `/openapi.json` did not provide a usable OpenAPI specification.
- Ollama/model-process resource telemetry is not captured by the current performance test.
- GPU and host-level resource telemetry are not captured.
- Cross-user isolation and session-expiration workflows remain limited.

These limitations are included in the coverage matrix and final reports.

---

## 23. Overall Strategy

The resulting QA strategy combines conventional automation with AI-specific evaluation:

```text
                Open WebUI
                    |
       +------------+------------+
       |            |            |
       v            v            v
      UI           API          AI
       |            |            |
       +------------+------------+
                    |
             Integration Tests
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
    Dependency  Concurrency  Performance
      Tests        Tests        Tests
        |
        v
  Reliability / Nondeterminism
        |
        v
 Golden Regression + Safety
        |
        v
     CI Quality Gate
        |
        v
      RCA / Evidence
```

The strategy is designed to provide maintainable, reusable, and evidence-driven QA coverage while explicitly distinguishing genuine application problems from AI variability, evaluator variance, test instability, infrastructure failures, and environment limitations.