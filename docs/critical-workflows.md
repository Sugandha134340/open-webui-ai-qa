# Critical Workflows

## 1. Purpose

This document defines the critical application and AI workflows selected for automation and evaluation in the Open WebUI v0.11.4 QA project.

The workflows were selected to provide coverage across:

- UI interaction
- API authorization
- AI generation
- AI evaluation
- dependency failures
- safety behavior
- concurrency
- performance
- reliability
- CI/CD quality gates

The goal is to prioritize meaningful workflows rather than creating a large number of shallow UI tests.

---

## 2. Workflow 1 — Application Availability

### Objective

Verify that the deployed Open WebUI instance is available and responding with the expected application version.

### Flow

```text
Test
  ↓
GET /api/version
  ↓
HTTP response
  ↓
Validate status
  ↓
Validate version
```

### Expected Behavior

The application should return:

```text
HTTP 200
version = 0.11.4
```

### Automation

Implemented through:

```text
tests/api/test_health.py
```

### Result

```text
PASS
```

---

## 3. Workflow 2 — Authentication and Authorization

### Objective

Verify that protected Open WebUI endpoints reject unauthenticated access.

### Flow

```text
Unauthenticated Request
        ↓
Protected API Endpoint
        ↓
Authorization Check
        ↓
Request Rejected
```

### Protected Operations Tested

```text
/api/chats
/api/chats/pinned
/api/chat/completions
```

### Expected Behavior

Unauthenticated requests must not be treated as authenticated application requests.

### Automation

Implemented through:

```text
tests/api/test_auth.py
tests/api/test_chat.py
tests/api/test_signin.py
```

### Result

The authorization and invalid-credential checks passed.

Positive authenticated access could not be reliably tested because valid QA credentials were unavailable in the local environment.

---

## 4. Workflow 3 — Browser Login Discovery

### Objective

Verify that the Open WebUI frontend correctly redirects an unauthenticated user to the authentication page.

### Flow

```text
Open WebUI
    ↓
Browser loads application
    ↓
Authentication redirect
    ↓
/auth?redirect=%2F
    ↓
Validate authentication page
```

### Browsers

The workflow is executed against:

```text
Chromium
Firefox
```

### Automation

Implemented through:

```text
tests/ui/test_login_discovery.py
```

### Result

```text
Chromium: PASS
Firefox:  PASS
```

---

## 5. Workflow 4 — Chat Page Discovery

### Objective

Verify the browser-level application routing behavior for an unauthenticated user attempting to access the chat interface.

### Flow

```text
Browser
  ↓
Open WebUI
  ↓
Authentication redirect
  ↓
Validate /auth route
  ↓
Observe application API requests
```

### Automation

Implemented through:

```text
tests/ui/test_chat_discovery.py
```

### Result

The workflow passes on:

```text
Chromium
Firefox
```

The test does not require `/api/version` to be observed before the authentication redirect because browser request ordering can vary across browsers.

---

## 6. Workflow 5 — Ollama Integration

### Objective

Verify that the AI backend is reachable and capable of serving the configured model.

### Flow

```text
QA Framework
     ↓
Ollama API
     ↓
Health / model availability
     ↓
Generation request
     ↓
AI response
```

### Validations

The integration layer verifies:

- Ollama connectivity
- service availability
- model availability
- text generation

### Automation

Implemented through:

```text
tests/integration/test_ollama_client.py
```

### Result

```text
4 integration tests
4 passed
```

---

## 7. Workflow 6 — AI Scenario Evaluation

### Objective

Evaluate AI behavior using structured scenarios rather than relying only on exact string matching.

### Flow

```text
AI Scenario Dataset
        ↓
Scenario Runner
        ↓
Ollama / AI Model
        ↓
Generated Response
        ↓
Rule-Based Evaluation
        +
Semantic Evaluation
        ↓
Pass / Fail / Error
        ↓
Report
```

### Dataset

The evaluation dataset contains:

```text
35 scenarios
```

The scenarios cover:

- normal requests
- edge cases
- ambiguous requests
- contradictory instructions
- out-of-scope requests
- prompt injection
- safety
- groundedness
- consistency
- multi-turn behavior
- long input
- instruction following
- hallucination
- robustness

### Automation

Implemented through:

```text
framework/evaluators/
datasets/ai_scenarios.json
reports/ai_scenario_results.json
```

---

## 8. Workflow 7 — AI Safety and Adversarial Testing

### Objective

Verify that the AI evaluation framework detects unsafe or inappropriate behavior.

### Scenarios Include

```text
Prompt injection
Instruction override
System/developer instruction extraction
Fake system messages
Secret exposure requests
Explosive-related requests
Credential bypass
Phishing
```

### Flow

```text
Adversarial Scenario
        ↓
AI Model
        ↓
Observable Response
        ↓
Safety Evaluator
        ↓
Safety Result
```

Safety failures are tracked separately from ordinary AI-quality results.

---

## 9. Workflow 8 — Dependency Failure Handling

### Objective

Verify that AI/backend dependency failures are detected and do not appear as successful AI responses.

### Failure Conditions

The dependency test suite covers:

```text
HTTP 500
Timeout
Malformed response
Empty response
Unavailable dependency
HTTP 429 / rate limiting
Partial response
```

### Flow

```text
Test Scenario
     ↓
Simulated Dependency Failure
     ↓
Ollama Client
     ↓
Error Handling
     ↓
Validated Failure Result
```

### Automation

Implemented through:

```text
tests/integration/test_dependency_failures.py
```

### Result

```text
7 dependency tests
7 passed
```

---

## 10. Workflow 9 — Golden AI Regression

### Objective

Detect regressions in known AI behaviors using a fixed golden dataset.

### Flow

```text
Golden Scenario
      ↓
AI Response
      ↓
Evaluation
      ↓
Expected Result
      ↓
Regression Detection
```

### Regression Examples

The regression suite validates:

- precision/recall response
- arithmetic correctness
- exact output requirements

It also intentionally introduces incorrect outputs to verify that the evaluation system detects the regression.

### Automation

Implemented through:

```text
datasets/golden_dataset.json
tests/regression/test_ai_regression.py
```

---

## 11. Workflow 10 — Nondeterminism Testing

### Objective

Determine whether repeated executions of important AI scenarios remain consistent.

### Flow

```text
Scenario
   ↓
Run 1
Run 2
...
Run 10
   ↓
Compare Results
   ↓
Determine Stability
```

### Scenarios

The repeated-run evaluation includes:

```text
AI026 — factual consistency
AI027 — arithmetic consistency
AI028 — date/time consistency
```

### Result

```text
Scenarios: 3
Runs per scenario: 10
Total executions: 30
Stable passes: 30
Errors: 0
```

---

## 12. Workflow 11 — Reliability and Flakiness

### Objective

Measure whether the regression suite itself behaves reliably across repeated executions.

### Flow

```text
Regression Suite
      ↓
Run 1
Run 2
...
Run 10
      ↓
Collect:
- status
- duration
- stdout/stderr
- return code
      ↓
Classify failures
```

### Result

```text
Total runs: 10
Passed: 7
Failed: 3
Pass rate: 70%
Retries: 0
Average runtime: ~15.89s
```

The observed failures were associated with AI001 and were classified as evaluator/judge variance based on the additional evidence collected.

---

## 13. Workflow 12 — Concurrent AI Requests

### Objective

Verify that multiple simultaneous AI requests can be processed without observed request failures.

### Flow

```text
             +--> Request 1
             |
             +--> Request 2
             |
Test --------+--> Request 3
             |
             +--> Request 4
             |
             +--> Request 5
                    ↓
              Collect Results
                    ↓
              Validate Invariant
```

### Expected Invariant

Every submitted request should produce a valid non-empty response without an unexpected request failure.

### Result

```text
Concurrent requests: 5
Successful: 5
Failed: 0
```

### Automation

Implemented through:

```text
tests/concurrency/test_ollama_concurrency.py
```

---

## 14. Workflow 13 — Performance and Load

### Objective

Measure AI response latency as concurrency increases.

### Concurrency Levels

```text
1
3
5
10
```

### Metrics

The test records:

- average latency
- P50 latency
- P95 latency
- wall-clock duration
- error rate
- concurrency
- resource samples

### Flow

```text
Increase Concurrency
        ↓
Send AI Requests
        ↓
Measure Latency
        ↓
Measure Errors
        ↓
Compare P50/P95
        ↓
Identify Degradation
```

### Result

The tested configuration showed increased latency at higher concurrency, particularly at concurrency 10.

No breaking point was observed within the tested range of 1–10 concurrent requests.

---

## 15. Workflow 14 — Persistent Storage and Restart Recovery

### Objective

Verify that the Open WebUI runtime can recover after a container restart while retaining its persistent storage configuration.

### Flow

```text
Running Container
      ↓
Inspect Docker Volume
      ↓
Restart Container
      ↓
Wait for Healthy State
      ↓
Call /api/version
      ↓
Validate HTTP 200
```

### Storage

The application data volume is mounted at:

```text
/app/backend/data
```

### Result

```text
Container: healthy
/api/version: HTTP 200
Version: 0.11.4
```

Authenticated individual records could not be validated because valid QA credentials were unavailable.

---

## 16. Workflow 15 — CI Quality Gate

### Objective

Verify that the CI pipeline detects a deliberately introduced regression.

### Flow

```text
Code Change
    ↓
Push
    ↓
GitHub Actions
    ↓
Tests
    ↓
Quality Gate
    ↓
Failure
    ↓
Build Blocked
```

A test assertion was intentionally changed to create a regression.

The CI pipeline detected the failure.

The assertion was then restored and the quality gate returned to the expected passing state.

### Automation

Implemented through:

```text
.github/workflows/ci.yml
tests/ci/test_quality_gate.py
```

---

## 17. Workflow 16 — Root-Cause Analysis

### Objective

Investigate significant failures using evidence rather than reporting only the observed symptom.

### RCA Flow

```text
Failure
  ↓
Expected Behavior
  ↓
Actual Behavior
  ↓
Reproduction
  ↓
Evidence
  ↓
Affected Component
  ↓
Root Cause / Classification
  ↓
Prevention
  ↓
Regression Test
```

### RCA Cases

The project documents five significant cases:

1. AI020 — secret exposure handling
2. AI015 — contradictory instruction handling
3. AI008 — long-output timeout
4. AI001 — semantic evaluation flakiness
5. Authenticated API access — environment limitation

Detailed analysis is maintained in:

```text
docs/rca-report.md
```

---

## 18. Workflow Coverage Summary

| Workflow | Automation | Result |
|---|---|---|
| Application availability | API | PASS |
| Authentication rejection | API | PASS |
| Browser login discovery | UI | PASS |
| Chat route discovery | UI | PASS |
| Ollama integration | Integration | PASS |
| AI scenario evaluation | AI framework | Completed |
| Safety/adversarial evaluation | AI framework | Completed |
| Dependency failures | Integration | 7/7 PASS |
| Golden regression | Regression | Implemented |
| Nondeterminism | AI reliability | 30/30 stable |
| Regression reliability | Reliability | 10 runs |
| Concurrent requests | Concurrency | 5/5 PASS |
| Performance/load | Performance | 1–10 concurrency |
| Restart recovery | Backend | PASS |
| CI quality gate | CI/CD | Demonstrated |
| RCA | Quality analysis | 5 cases |

---

## 19. Known Workflow Limitations

The following workflows could not be fully completed because of environment limitations:

- positive authenticated Open WebUI workflows
- authenticated streaming/real-time E2E
- authenticated chat/history persistence
- multi-user isolation
- session-expiration testing
- OpenAPI contract testing

These limitations are explicitly recorded in the coverage matrix and are not represented as successful tests.