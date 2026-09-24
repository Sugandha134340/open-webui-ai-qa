# Test Coverage Matrix

## 1. Purpose

This document maps the assignment requirements to the implemented test automation framework, execution evidence, and known limitations.

The purpose of the matrix is to provide traceability between:

- Assignment requirements
- Test categories
- Implemented tests
- Test evidence
- Current coverage status
- Known limitations

Coverage is classified as:

- **Complete** — the required behavior has been implemented and executed.
- **Partial** — meaningful coverage exists, but one or more important paths remain unavailable or unvalidated.
- **Limited** — the area was investigated or partially exercised, but full validation was not possible.
- **Not Applicable** — the selected application or available interface does not support the required behavior in the tested configuration.

---

## 2. Application Selection and Architecture

| Requirement Area | Coverage | Implementation / Evidence | Status / Limitation |
|---|---|---|---|
| Application selection | Complete | Open WebUI v0.11.4 selected as the application under test | Completed |
| Application architecture | Complete | `docs/architecture.md` | Completed |
| Critical workflows | Complete | `docs/critical-workflows.md` | Completed |
| Test architecture | Complete | pytest + Playwright + AI evaluation framework | Completed |
| Local reproducible environment | Complete | Dockerized Open WebUI + local Ollama | Completed |
| CI execution | Complete | GitHub Actions workflow | Completed |

---

## 3. UI and E2E Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status / Limitation |
|---|---|---|---|
| Unauthenticated application access | Complete | `tests/ui/test_chat_discovery.py` | Passed |
| Authentication redirect | Complete | Playwright redirect assertion | Passed |
| Invalid login | Complete | `tests/ui/test_login_discovery.py` | Passed |
| Authentication API request observation | Complete | Playwright request interception | Passed |
| Chromium coverage | Complete | Playwright Chromium | Passed |
| Firefox coverage | Complete | Playwright Firefox | Passed |
| Cross-browser execution | Complete | Chromium + Firefox parameterization | Passed |
| Authenticated positive workflow | Partial | Protected endpoints tested without credentials | Valid QA credentials unavailable |
| Authenticated chat workflow | Limited | Could not reliably execute authenticated workflow | Credentials unavailable |
| Real-time authenticated E2E | Limited | Streaming/real-time path could not be fully exercised | Requires authenticated application path |

### Latest UI Result

```text
Total UI tests: 4
Passed: 4
Failed: 0

Covered workflows:

```text
Chromium:
    Unauthenticated redirect    PASS
    Invalid login               PASS

Firefox:
    Unauthenticated redirect    PASS
    Invalid login               PASS

```

## 4. API and Backend Coverage

| Requirement Area | Coverage | Implementation / Evidence | Result / Limitation |
|---|---|---|---|
| API availability | Complete | `tests/api/test_health.py` | PASS |
| Application version endpoint | Complete | `/api/version` | PASS |
| Unauthenticated API access | Complete | `tests/api/test_auth.py` | PASS |
| Protected chats endpoint | Complete | `test_chats_requires_authentication` | PASS |
| Protected pinned chats endpoint | Complete | `test_pinned_chats_requires_authentication` | PASS |
| Chat completion authorization | Complete | `tests/api/test_chat.py` | PASS |
| Invalid credentials | Complete | `tests/api/test_signin.py` | PASS |
| Authenticated API access | Partial | `tests/api/test_authenticated_access.py` | Blocked by unavailable valid QA credentials |
| API schema / contract validation | Limited | `/openapi.json` investigated | No valid OpenAPI document available |
| Backend service connectivity | Complete | Ollama integration tests | PASS |
| Dependency error handling | Complete | `tests/integration/test_dependency_failures.py` | 7/7 PASS |
| Persistent storage | Partial | Docker volume inspection and restart recovery | Recovery verified; authenticated record integrity not validated |

### Latest API Test Result

```text
Total API tests: 6
Passed: 5
Failed: 1
```

The single failure is the positive authenticated-access test. The local environment did not provide valid QA credentials; the sign-in attempt returned an invalid-credentials response. This is therefore treated as an environment limitation rather than an observed application regression.

### Authorization Coverage

The following protected API behavior was successfully validated:

```text
/api/chats          → unauthenticated request rejected
/api/chats/pinned   → unauthenticated request rejected
/api/chat/completions → unauthenticated request rejected
```

Invalid login credentials were also rejected successfully.

### Health and Version Validation

The application health/version endpoint returned:

```text
HTTP 200
Content-Type: application/json
Version: 0.11.4
```

This verifies that the deployed Open WebUI instance was reachable and responding with the expected application version.

### OpenAPI Limitation

The following endpoint was investigated:

```text
http://localhost:3000/openapi.json
```

Although it returned HTTP 200, the response content was frontend HTML rather than an OpenAPI specification.

Therefore, contract tests were not created against this response because doing so would require inventing an API schema that was not actually available from the running application.

### Backend and Persistence Coverage

The Open WebUI container uses a persistent Docker volume mounted at:

```text
/app/backend/data
```

Container restart recovery was validated. After restart, the container returned to a healthy state and `/api/version` continued to return HTTP 200.

Individual authenticated users, chats, and records could not be validated for persistence because valid QA credentials were unavailable.

### API Coverage Assessment

The API/backend layer has meaningful coverage for:

- Health and version checks
- Authentication rejection
- Protected endpoint authorization
- Invalid credentials
- Backend Ollama connectivity
- Dependency failure handling
- Docker-backed persistence and restart recovery

The main remaining limitation is positive authenticated API coverage, which depends on obtaining valid QA credentials.

## 5. Dependency Failure Coverage

| Failure Scenario | Coverage | Test | Result |
|---|---|---|---|
| HTTP 500 | Complete | `test_dependency_http_500_is_detected` | PASS |
| Timeout | Complete | `test_dependency_timeout_is_detected` | PASS |
| Malformed response | Complete | `test_dependency_malformed_response_is_detected` | PASS |
| Empty response | Complete | `test_dependency_empty_response_is_handled` | PASS |
| Dependency unavailable | Complete | `test_dependency_unavailable_is_detected` | PASS |
| Rate limiting / HTTP 429 | Complete | `test_dependency_rate_limit_is_detected` | PASS |
| Partial response | Complete | `test_dependency_partial_response_is_handled` | PASS |

### Latest Dependency Test Result

```text
Total dependency tests: 7
Passed: 7
Failed: 0

The dependency tests validate that the framework can detect and handle realistic upstream failure conditions without treating malformed, incomplete, unavailable, or unsuccessful dependency responses as successful AI results.

## 6. Ollama Integration Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status |
|---|---|---|---|
| Ollama client configuration | Complete | `tests/integration/test_ollama_client.py` | PASS |
| Ollama health check | Complete | `tests/integration/test_ollama_client.py` | PASS |
| Model availability | Complete | `tests/integration/test_ollama_client.py` | PASS |
| Ollama text generation | Complete | `tests/integration/test_ollama_client.py` | PASS |
| Ollama dependency connectivity | Complete | Local Ollama service | PASS |

### Latest Ollama Integration Result

```text
Total integration tests: 4
Passed: 4
Failed: 0
```

The integration tests verified that the configured Ollama service was reachable, the expected model was available, and a generation request could be completed successfully.

---

## 7. AI Evaluation Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status / Limitation |
|---|---|---|---|
| AI scenario dataset | Complete | `datasets/ai_scenarios.json` | 35 scenarios |
| 30+ AI scenarios | Complete | 35 scenarios | Completed |
| Normal prompts | Complete | AI001–AI005 | Covered |
| Edge cases | Complete | AI006–AI010 | Covered |
| Ambiguous prompts | Complete | AI011–AI013 | Covered |
| Contradictory instructions | Complete | AI014–AI015 | Covered |
| Out-of-scope requests | Complete | AI016–AI017 | Covered |
| Prompt injection | Complete | AI018–AI020 | Covered |
| Safety | Complete | AI021–AI023 | Covered |
| Groundedness | Complete | AI024–AI025 | Covered |
| Consistency | Complete | AI026–AI028 | Covered |
| Multi-turn behavior | Complete | AI029–AI030 | Covered |
| Long input | Complete | AI031 | Covered |
| Instruction following | Complete | AI032–AI033 | Covered |
| Hallucination | Complete | AI034 | Covered |
| Robustness | Complete | AI035 | Covered |
| Rule-based evaluation | Complete | `framework/evaluators/rule_based.py` | Implemented |
| Semantic evaluation | Complete | `framework/evaluators/semantic_evaluator.py` | Implemented |
| Combined evaluation | Complete | `framework/evaluators/ai_evaluator.py` | Implemented |
| Safety evaluation | Complete | AI evaluator safety checks | Implemented |
| Arithmetic validation | Complete | Deterministic arithmetic evaluator | Implemented |
| Structure validation | Complete | Structure evaluator | Implemented |
| Exact-match evaluation | Complete | Rule-based evaluator | Implemented |

### AI Baseline Result

```text
Total scenarios:       35
Passed:                21
Failed:                13
Errors:                 1
Evaluated:             34
Pass rate:          61.76%
Average latency:      9.55s
```

The baseline results are stored in:

```text
reports/ai_scenario_results.json
```

The baseline is treated as an evaluation snapshot rather than as a universal quality score.

---

## 8. Golden Dataset and Regression Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status |
|---|---|---|---|
| Golden dataset | Complete | `datasets/golden_dataset.json` | Completed |
| Golden precision/recall response | Complete | `tests/regression/test_ai_regression.py` | Implemented |
| Golden arithmetic response | Complete | `tests/regression/test_ai_regression.py` | Implemented |
| Deliberate arithmetic regression | Complete | Regression test | Detected |
| Golden exact-output response | Complete | Regression test | Implemented |
| Deliberate exact-output regression | Complete | Regression test | Detected |
| Regression execution | Complete | pytest | Completed |

### Regression Coverage

The regression suite contains five checks:

```text
1. Golden precision/recall response
2. Golden arithmetic response
3. Deliberate arithmetic regression detection
4. Golden exact-output response
5. Deliberate exact-output regression detection
```

A successful isolated execution produced:

```text
5 passed
```

### AI001 Reliability Observation

The AI001 golden response is deterministic and factually correct.

A direct evaluation of the same response produced:

```text
Overall score: 1.0
Semantic score: 1.0
Rule-based score: 1.0
Passed: True
```

However, repeated reliability execution showed intermittent semantic-judge failures.

This behavior is classified as evaluator/judge variance rather than a demonstrated regression in the golden response.

---

## 9. Semantic Judge Validation

| Requirement Area | Coverage | Evidence | Result |
|---|---|---|---|
| Judge validation dataset | Complete | `datasets/judge_validation.json` | 12 cases |
| Human-labeled validation | Complete | Judge validation dataset | 12 cases |
| Correct judgments | Complete | Validation execution | 10 |
| False positives | Complete | Validation execution | 2 |
| False negatives | Complete | Validation execution | 0 |

### Judge Validation Result

```text
Validation cases: 12
Correct judgments: 10
False positives: 2
False negatives: 0
Validation rate: 83.33%
```

This result represents the observed performance of the implemented semantic judge on the validation dataset and is not treated as a universal accuracy guarantee.

---

## 10. Nondeterminism Coverage

| Requirement Area | Coverage | Implementation / Evidence | Result |
|---|---|---|---|
| Repeated AI execution | Complete | `framework/evaluators/nondeterminism_runner.py` | Completed |
| Factual consistency | Complete | AI026 | Stable |
| Arithmetic consistency | Complete | AI027 | Stable |
| Time/date consistency | Complete | AI028 | Stable |
| Repeated executions | Complete | 10 repetitions per scenario | Completed |
| Error tracking | Complete | Nondeterminism report | Completed |

### Nondeterminism Result

```text
Scenarios evaluated: 3
Repetitions per scenario: 10
Total executions: 30
Stable passes: 30
Errors: 0
```

The tested scenarios therefore produced:

```text
30 / 30 stable passes
```

This result applies to the tested scenarios, model, runtime configuration, and evaluation conditions.

---

## 11. Reliability and Flakiness Coverage

| Requirement Area | Coverage | Implementation / Evidence | Result |
|---|---|---|---|
| Repeated suite execution | Complete | `tests/regression/run_reliability.py` | 10 runs |
| Pass/failure tracking | Complete | Reliability report | Completed |
| Execution-time tracking | Complete | Reliability report | Completed |
| Retry tracking | Complete | No retries used | Completed |
| Flakiness detection | Complete | Repeated AI regression | Detected |
| Failure classification | Complete | RCA analysis | Completed |
| AI evaluator variance | Complete | AI001 repeated failures | Identified |

### Reliability Result

```text
Total runs:       10
Passed runs:       7
Failed runs:       3
Pass rate:        70%
Failure rate:     30%
Retries:           0
Average runtime: ~15.89s
```

All three observed failures were associated with AI001.

The remaining four regression checks remained stable across all 10 runs.

```text
Other regression checks:
4 / 4 stable across 10 runs
```

The AI001 behavior is classified as semantic evaluator/judge variance.

Automatic retries were not used to hide the observed failures.

---

## 12. Concurrency Coverage

| Requirement Area | Coverage | Implementation / Evidence | Result |
|---|---|---|---|
| Concurrent AI requests | Complete | `tests/concurrency/test_ollama_concurrency.py` | Completed |
| Five simultaneous requests | Complete | Concurrency test | 5/5 successful |
| Failure tracking | Complete | Concurrency report | 0 failures |
| Wall-clock measurement | Complete | Concurrency test | Recorded |

### Concurrency Result

```text
Concurrent requests: 5
Successful requests: 5
Failed requests:     0
```

The concurrency test completed without observed request failures.

---

## 13. Performance Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status |
|---|---|---|---|
| Increasing concurrency | Complete | `tests/performance/test_ollama_load.py` | 1, 3, 5, 10 |
| Average latency | Complete | Performance report | Recorded |
| P50 latency | Complete | Performance report | Recorded |
| P95 latency | Complete | Performance report | Recorded |
| Error rate | Complete | Performance report | Recorded |
| Wall-clock time | Complete | Performance report | Recorded |
| Resource sampling | Partial | Docker stats | Open WebUI container only |
| Breaking-point analysis | Complete within tested range | 1–10 concurrency | No breaking point observed |

### Latest Performance Results

| Concurrency | Average | P50 | P95 | Wall Time | Error Rate |
|---:|---:|---:|---:|---:|---:|
| 1 | 10.77s | 10.77s | 10.77s | 11.14s | 0% |
| 3 | 4.31s | 4.32s | 5.42s | 6.00s | 0% |
| 5 | 5.13s | 4.97s | 7.16s | 8.04s | 0% |
| 10 | 8.10s | 8.30s | 12.46s | 14.06s | 0% |

### Performance Interpretation

The tested configuration showed increased latency at higher concurrency levels, particularly at concurrency 10.

No breaking point was observed within the tested range of 1–10 concurrent requests.

The concurrency-1 result is treated as a warm-up/variability observation rather than evidence of a monotonic latency relationship.

---

## 14. Resource Telemetry Coverage

| Requirement Area | Coverage | Evidence | Status / Limitation |
|---|---|---|---|
| CPU sampling | Partial | Docker stats | Open WebUI container |
| Memory sampling | Partial | Docker stats | Open WebUI container |
| Memory percentage | Partial | Docker stats | Open WebUI container |
| Sample collection | Complete | Performance test | Implemented |
| Ollama process telemetry | Not covered | AI requests go directly to Ollama | Not captured |
| GPU telemetry | Not covered | No GPU telemetry configured | Not captured |
| Host-level telemetry | Not covered | No host resource collector configured | Not captured |

The performance framework currently samples the `open-webui` Docker container.

Because the AI benchmark sends requests directly to Ollama, Open WebUI container telemetry does not represent complete resource consumption of the Ollama/model process.

---

## 15. Persistent Storage and Recovery Coverage

| Requirement Area | Coverage | Evidence | Status |
|---|---|---|---|
| Persistent Docker volume | Complete | Docker inspection | Verified |
| `/app/backend/data` mount | Complete | Docker inspection | Verified |
| Container restart | Complete | Manual restart test | Completed |
| Health recovery | Complete | Docker health status | Healthy |
| Application recovery | Complete | `/api/version` | HTTP 200 |
| Authenticated user data persistence | Limited | Requires valid credentials | Not directly validated |
| Authenticated chat persistence | Limited | Requires valid credentials | Not directly validated |

### Recovery Result

After restarting the Open WebUI container:

```text
Container health: healthy
/api/version: HTTP 200
Version: 0.11.4
```

Individual authenticated records could not be validated because valid QA credentials were unavailable.

---

## 16. Security and Privacy Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status |
|---|---|---|---|
| Unauthorized access | Complete | API tests | Covered |
| Protected endpoint authorization | Complete | API tests | Covered |
| Invalid authentication | Complete | Sign-in tests | Covered |
| Prompt injection | Complete | AI018–AI020 | Covered |
| Secret exposure requests | Complete | AI020 | Covered |
| Credential bypass | Complete | AI022 | Covered |
| Phishing | Complete | AI023 | Covered |
| Sensitive-information handling | Complete | AI evaluation scenarios | Covered |
| Secrets in logs | Limited | No dedicated secret-log scanner | Not fully validated |
| Cross-user isolation | Limited | Requires authenticated multi-user setup | Not directly validated |
| Session expiration | Limited | Requires authenticated session workflow | Not directly validated |

The security coverage focuses on observable application and AI behavior and should not be interpreted as a complete penetration test.

---

## 17. Safety Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status |
|---|---|---|---|
| Dangerous request handling | Complete | AI021 | Covered |
| Credential bypass | Complete | AI022 | Covered |
| Phishing | Complete | AI023 | Covered |
| Secret exposure | Complete | AI020 | Covered |
| Prompt injection | Complete | AI018–AI020 | Covered |
| System/developer instruction extraction | Complete | AI018 | Covered |
| Fake system-message injection | Complete | AI019 | Covered |

Safety results are evaluated separately from ordinary semantic quality results.

---

## 18. CI/CD Coverage

| Requirement Area | Coverage | Implementation / Evidence | Status |
|---|---|---|---|
| GitHub Actions workflow | Complete | `.github/workflows/ci.yml` | Implemented |
| Automated test execution | Complete | CI workflow | Implemented |
| Quality gate | Complete | `tests/ci/test_quality_gate.py` | Implemented |
| Deliberate regression | Complete | Intentional assertion modification | Detected |
| Regression restoration | Complete | Assertion restored | Verified |
| Green CI validation | Complete | Restored pipeline | Verified |

### Deliberate CI Regression

The CI quality-gate assertion was intentionally changed from:

```python
assert result["passed"] is True
```

to:

```python
assert result["passed"] is False
```

This intentionally caused the quality gate to fail.

The assertion was then restored and the quality gate returned to the expected passing behavior.

This demonstrates that the CI pipeline can detect an introduced regression.

---

## 19. Root-Cause Analysis Coverage

| RCA Case | Classification | Confidence |
|---|---|---|
| AI020 secret exposure handling | AI/application behavior | High |
| AI015 contradictory instruction handling | AI/application behavior | High |
| AI008 long-output timeout | Dependency/runtime behavior | High for observed timeout |
| AI001 golden evaluation flakiness | Evaluator/judge variance | High |
| Authenticated API test | Environment limitation | High |

Detailed analysis is available in:

```text
docs/rca-report.md
```

The RCA process distinguishes observed evidence from assumptions about internal causes.

---

## 20. Real-Time / Streaming Coverage

| Requirement Area | Coverage | Status / Limitation |
|---|---|---|
| Real-time capability identified | Complete | Open WebUI supports AI streaming behavior |
| Authenticated streaming workflow | Limited | Valid credentials unavailable |
| Streaming failure injection | Limited | Full authenticated path unavailable |
| Alternative AI evaluation | Complete | 35-scenario AI evaluation framework |

Because the authenticated real-time workflow could not be fully exercised, deeper AI evaluation was used to provide additional coverage in the available environment.

---

## 21. OpenAPI / Contract Coverage

| Requirement Area | Coverage | Status |
|---|---|---|
| OpenAPI endpoint investigation | Complete | Investigated |
| OpenAPI document retrieval | Limited | Endpoint returned frontend HTML |
| OpenAPI schema validation | Not applicable in current environment | No valid OpenAPI specification available |
| Contract tests | Not implemented | Avoided invalid contract assumptions |

The endpoint:

```text
http://localhost:3000/openapi.json
```

returned HTTP 200 but with frontend HTML content rather than an OpenAPI document.

Therefore, no contract tests were created against the response.

---

## 22. Coverage Summary

### Completed Areas

The following major areas have meaningful implemented and executed coverage:

- Application selection
- Application architecture
- Critical workflows
- UI/E2E
- Chromium
- Firefox
- Authentication rejection behavior
- API authorization
- Ollama integration
- Dependency failures
- AI scenario evaluation
- 35-scenario AI dataset
- Golden dataset
- Semantic judge
- Judge validation
- Safety
- Prompt injection
- Groundedness
- Consistency
- Instruction following
- Hallucination
- Nondeterminism
- Golden regression
- Reliability
- Flakiness analysis
- Concurrency
- Performance
- CI/CD
- Deliberate CI regression
- RCA
- Persistent Docker volume recovery

### Partial or Limited Areas

The following areas remain constrained by the local environment:

- Positive authenticated Open WebUI workflows
- Authenticated chat/history persistence
- Authenticated real-time/streaming E2E
- OpenAPI contract testing
- Ollama/model-process resource telemetry
- GPU telemetry
- Host-level resource telemetry
- Cross-user isolation
- Session expiration
- Dedicated secret-log scanning

These limitations are explicitly documented rather than being represented as completed coverage.

---

## 23. Highest-Priority Remaining Coverage Gaps

The most important remaining gaps are:

1. Valid QA credentials for authenticated Open WebUI workflows.
2. Authenticated streaming/real-time E2E testing.
3. Multi-user authorization and isolation testing.
4. Session expiration testing.
5. Direct Ollama/model resource telemetry.
6. GPU and host-level performance telemetry.
7. A valid OpenAPI specification for contract testing.

These gaps are primarily environment or application-interface limitations rather than unreported test failures.