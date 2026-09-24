# Open WebUI AI Test Automation Framework

A comprehensive AI-focused test automation framework built for **Open WebUI v0.11.4**, covering UI/E2E testing, API and integration testing, dependency failures, AI response evaluation, safety testing, nondeterminism, regression detection, reliability, concurrency, performance, observability, root-cause analysis, and CI/CD quality gates.

---

## 1. Project Overview

This project was developed as an **AI Test Automation Engineer Intern assignment**.

The objective is to build a production-oriented quality engineering framework capable of validating both conventional application behavior and AI-specific behavior.

The framework covers:

- UI and end-to-end workflows
- API and authentication behavior
- Backend and integration behavior
- Dependency failures
- AI response quality
- Safety and prompt-injection behavior
- Groundedness and hallucination
- Instruction following
- Multi-turn behavior
- Nondeterminism
- Golden-response regression
- Reliability and flaky-test detection
- Concurrency
- Performance and latency
- Resource telemetry
- CI/CD quality gates
- Root-cause analysis
- Security and privacy considerations
- Persistent-storage recovery

---

## 2. Application Under Test

### Selected Application

**Open WebUI v0.11.4**

Open WebUI was selected as the application under test because it provides a realistic AI application surface with:

- Web-based user interface
- Authentication and protected routes
- Backend APIs
- LLM integration
- Streaming/real-time AI interaction
- Persistent application data
- External model dependency
- Multiple failure modes suitable for reliability and automation testing

### Local Deployment

The application was deployed locally using Docker.

```text
Open WebUI v0.11.4
        |
        v
Docker Container
        |
        +---- Host Port 3000 -> Container Port 8080
        |
        +---- /app/backend/data
        |       |
        |       v
        |   Persistent Docker Volume
        |
        +---- Ollama
                |
                +---- llama3.2:3b
```

The deployed application was verified through:

```text
GET /api/version
```

The application returned:

```json
{
  "version": "0.11.4",
  "deployment_id": ""
}
```

The Docker container was also verified to use a persistent volume mounted at:

```text
/app/backend/data
```

### Application Verification

Container restart recovery was validated by restarting the Open WebUI container and verifying that:

- The container returned to a healthy state.
- The application became available again.
- `/api/version` returned HTTP 200.
- The application continued to report version `0.11.4`.

### AI Runtime

The AI evaluation framework uses the locally available Ollama service.

```text
Ollama
   |
   +---- llama3.2:3b
```

Direct Ollama generation was verified independently before running the AI evaluation and performance tests.

### Authentication Limitation

The local environment did not provide valid QA credentials for an authenticated Open WebUI user.

Therefore:

- Unauthenticated authorization behavior was tested.
- Invalid-login behavior was tested.
- Protected endpoints were verified to reject unauthenticated requests.
- Positive authenticated workflows could not be reliably executed.
- Individual authenticated user/chat persistence could not be directly validated.

This limitation is documented in the coverage matrix and final reports rather than bypassed or hidden.

### OpenAPI Limitation

The expected OpenAPI endpoint was investigated.

A request to:

```text
http://localhost:3000/openapi.json
```

returned HTTP 200, but the response content was the Open WebUI frontend HTML rather than an OpenAPI specification.

Therefore, contract tests were not created against this response, since treating the returned HTML as an API specification would produce invalid test coverage.

---

## 3. Technology Stack

| Area | Technology |
|---|---|
| Application | Open WebUI v0.11.4 |
| Containerization | Docker |
| Test Framework | pytest |
| Programming Language | Python 3.13.3 |
| UI Automation | Playwright |
| Browsers | Chromium, Firefox |
| AI Runtime | Ollama |
| AI Model | llama3.2:3b |
| AI Evaluation | Rule-based + semantic evaluation |
| Test Data | JSON |
| CI/CD | GitHub Actions |
| Version Control | Git / GitHub |
| Performance Testing | Python concurrency/load runner |
| Resource Telemetry | Docker stats |

---

## 4. Project Structure

```text
open-webui-ai-qa/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── datasets/
│   ├── ai_scenarios.json
│   ├── golden_dataset.json
│   └── judge_validation.json
│
├── docs/
│   ├── application-selection.md
│   ├── architecture.md
│   ├── critical-workflows.md
│   ├── test-strategy.md
│   ├── coverage-matrix.md
│   ├── rca-report.md
│   └── ai-usage-disclosure.md
│
├── framework/
│   ├── clients/
│   │   ├── openwebui_client.py
│   │   └── ollama_client.py
│   │
│   ├── evaluators/
│   │   ├── rule_based.py
│   │   ├── ai_evaluator.py
│   │   ├── semantic_evaluator.py
│   │   ├── dataset_loader.py
│   │   ├── evaluation_runner.py
│   │   ├── judge_validator.py
│   │   ├── ai_scenario_runner.py
│   │   ├── nondeterminism_runner.py
│   │   └── quality_drift.py
│   │
│   └── utils/
│
├── tests/
│   ├── ai/
│   ├── api/
│   ├── ci/
│   ├── concurrency/
│   ├── e2e/
│   ├── integration/
│   ├── performance/
│   ├── regression/
│   └── ui/
│
├── reports/
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 5. Test Architecture

The framework separates conventional application testing from AI-specific evaluation.

```text
                         +----------------------+
                         |      Pytest          |
                         |   Test Execution     |
                         +----------+-----------+
                                    |
        +---------------------------+---------------------------+
        |                           |                           |
        v                           v                           v
+---------------+           +---------------+           +---------------+
|   UI / E2E    |           | API / Backend |           | Integration   |
|   Playwright  |           |     Tests     |           | / Dependency |
+-------+-------+           +-------+-------+           +-------+-------+
        |                           |                           |
        v                           v                           v
+---------------+           +---------------+           +---------------+
| Open WebUI    |           | Open WebUI    |           | Ollama /     |
| Browser       |           | HTTP APIs     |           | Failure Mocks|
+---------------+           +---------------+           +---------------+

                         AI Evaluation Layer
                                  |
             +--------------------+--------------------+
             |                    |                    |
             v                    v                    v
      +-------------+      +-------------+      +-------------+
      | Rule-Based  |      |  Semantic   |      |   Golden    |
      | Evaluation  |      |   Judge     |      | Regression  |
      +-------------+      +-------------+      +-------------+
             |                    |                    |
             +--------------------+--------------------+
                                  |
                                  v
                    +----------------------------+
                    | Reliability / Nondeterminism|
                    | / RCA / Quality Analysis    |
                    +----------------------------+
```

### Major Test Layers

#### UI / E2E

Implemented using Playwright.

Covers:

- Unauthenticated access
- Authentication redirects
- Invalid login behavior
- Browser-level application behavior
- API requests triggered by the UI
- Cross-browser behavior

#### API / Backend

Covers:

- Authentication requirements
- Protected API access
- Unauthorized requests
- Invalid authentication
- Health/version behavior
- Chat endpoint authorization

#### Integration

Covers:

- Ollama client configuration
- Ollama health
- Model availability
- AI generation
- Dependency failures

#### AI Evaluation

The AI evaluation layer combines:

- Deterministic rule-based checks
- Semantic evaluation
- Safety evaluation
- Groundedness checks
- Hallucination checks
- Consistency checks
- Instruction-following checks
- Golden regression testing

#### Reliability

The reliability layer evaluates:

- Repeated test execution
- Flaky behavior
- Nondeterminism
- AI evaluator variance
- Retry behavior
- Performance under concurrency

---

## 6. Critical Workflows

The major workflows selected for automation are:

### Workflow 1: Unauthenticated Application Access

```text
Open WebUI
    |
    v
Access application
    |
    v
Authentication required
    |
    v
Redirect to /auth
```

### Workflow 2: Invalid Login

```text
Authentication page
        |
        v
Enter invalid credentials
        |
        v
POST /api/v1/auths/signin
        |
        v
Authentication rejected
        |
        v
User remains on authentication page
```

### Workflow 3: Protected API Access

```text
Unauthenticated request
        |
        v
Protected API endpoint
        |
        v
HTTP 401 / authorization failure
```

### Workflow 4: AI Generation

```text
Test scenario
      |
      v
Ollama client
      |
      v
llama3.2:3b
      |
      v
Generated response
      |
      v
AI evaluation
      |
      +---- Rule-based checks
      |
      +---- Semantic judge
      |
      +---- Safety / structure checks
```

### Workflow 5: Dependency Failure

```text
AI client
   |
   v
Dependency
   |
   +---- HTTP 500
   +---- Timeout
   +---- Malformed response
   +---- Empty response
   +---- Unavailable
   +---- Rate limit
   +---- Partial response
   |
   v
Failure handling
```

---

## 7. UI / E2E Testing

The UI suite uses Playwright with both Chromium and Firefox.

### Covered Scenarios

- Unauthenticated application redirect
- Invalid login
- Authentication route behavior
- API request observation
- Cross-browser execution

### Latest UI Result

```text
4 passed
```

Coverage:

```text
Chromium:
    Unauthenticated redirect       PASS
    Invalid login                  PASS

Firefox:
    Unauthenticated redirect       PASS
    Invalid login                  PASS
```

### UI Test Command

```powershell
pytest tests/ui -v
```

---

## 8. API and Backend Testing

The API tests validate authorization and protected application behavior.

### Covered Cases

- Protected chat endpoint requires authentication
- Protected pinned-chat endpoint requires authentication
- Chat completion requires authentication
- Invalid sign-in credentials are rejected
- Open WebUI version endpoint is accessible

### Authentication Limitation

The local environment did not provide valid credentials for a positive authenticated workflow.

The following behavior was therefore validated:

```text
Unauthenticated request
        |
        v
Protected endpoint
        |
        v
Authentication required
```

A positive authenticated user workflow is documented as an environment limitation rather than being simulated as a successful result.

### API Test Command

```powershell
pytest tests/api -v
```

---

## 9. Dependency Failure Testing

The dependency-failure framework covers realistic failure conditions.

### Tested Failure Modes

| Failure Type | Covered |
|---|---|
| HTTP 500 | Yes |
| Timeout | Yes |
| Malformed response | Yes |
| Empty response | Yes |
| Dependency unavailable | Yes |
| HTTP 429 / Rate limit | Yes |
| Partial response | Yes |

### Latest Result

```text
7 passed
```

### Test Command

```powershell
pytest tests/integration/test_dependency_failures.py -v
```

The tests use controlled responses and failure conditions to verify that the client does not silently treat dependency failures as successful AI responses.

---

## 10. AI Evaluation Framework

The AI evaluation framework combines deterministic and semantic techniques.

### Evaluation Methods

Depending on the scenario, the framework supports:

- Exact matching
- Structure validation
- Rule-based evaluation
- Semantic evaluation
- Semantic + rule-based evaluation
- Safety evaluation
- Code validation
- Groundedness evaluation
- Hallucination detection
- Consistency evaluation
- Contextual evaluation
- Robustness evaluation
- Arithmetic validation

The framework intentionally does not rely exclusively on an LLM judge.

Deterministic checks are used whenever the expected behavior can be validated deterministically.

---

## 11. AI Scenario Dataset

The main AI dataset contains:

```text
35 scenarios
```

The scenarios cover:

| Category | Scenarios |
|---|---|
| Normal | AI001–AI005 |
| Edge cases | AI006–AI010 |
| Ambiguous | AI011–AI013 |
| Contradictory | AI014–AI015 |
| Out of scope | AI016–AI017 |
| Prompt injection | AI018–AI020 |
| Safety | AI021–AI023 |
| Groundedness | AI024–AI025 |
| Consistency | AI026–AI028 |
| Multi-turn | AI029–AI030 |
| Long input | AI031 |
| Instruction following | AI032–AI033 |
| Hallucination | AI034 |
| Robustness | AI035 |

Dataset location:

```text
datasets/ai_scenarios.json
```

---

## 12. AI Evaluation Baseline

The initial full AI scenario evaluation produced:

```text
Total scenarios:       35
Passed:                21
Failed:                13
Errors:                 1
Evaluated:             34
Pass rate:          61.76%
Average latency:      9.55s
```

The pass rate is calculated among evaluated scenarios:

```text
21 / 34 = 61.76%
```

The result is treated as a baseline rather than as a single overall quality score.

Individual failures were analyzed to distinguish between:

- Actual AI/application behavior
- Evaluator/judge variance
- Infrastructure/runtime issues
- Test/evaluation design issues

---

## 13. Golden Dataset

A separate golden dataset is used for regression protection.

Location:

```text
datasets/golden_dataset.json
```

The regression suite covers important deterministic behaviors including:

- Precision and recall explanation
- Arithmetic correctness
- Exact-output instruction following
- Deliberate incorrect arithmetic detection
- Deliberate incorrect exact-output detection

### Regression Tests

The regression suite contains five checks:

```text
1. Golden precision/recall response
2. Golden arithmetic response
3. Deliberate arithmetic regression detection
4. Golden exact-output response
5. Deliberate exact-output regression detection
```

A successful run produces:

```text
5 passed
```

---

## 14. Semantic Judge Validation

The semantic evaluator uses a local Ollama model as a judge for scenarios where deterministic evaluation alone is insufficient.

Judge validation is performed using:

```text
datasets/judge_validation.json
```

Validation result:

```text
Validation cases: 12
Correct judgments: 10
False positives:    2
False negatives:    0
Validation rate: 83.33%
```

This result describes the behavior of the implemented judge-validation dataset and should not be interpreted as a universal accuracy guarantee for the semantic evaluator.

---

## 15. Nondeterminism Testing

Nondeterminism was evaluated using repeated executions of selected AI scenarios.

The framework evaluates scenarios such as:

- Factual consistency
- Arithmetic consistency
- Time/date-related consistency

The nondeterminism runner executes selected scenarios repeatedly and records:

- Individual results
- Pass/fail status
- Errors
- Stability across repetitions

### Result

```text
Scenarios evaluated: 3
Repetitions per scenario: 10
Total executions: 30
Stable passes: 30
Errors: 0
```

The selected nondeterminism checks therefore produced:

```text
30 / 30 stable passes
```

This result applies only to the tested scenarios and configuration.

---

## 16. AI Regression Reliability

The regression suite was executed repeatedly to measure reliability.

### Reliability Experiment

```text
Total runs:       10
Passed runs:       7
Failed runs:       3
Pass rate:        70%
Failure rate:     30%
Retries:           0
Average runtime: ~15.89s
```

All three observed failures were associated with the AI001 precision/recall golden evaluation.

The remaining four regression checks remained stable across the repeated executions.

```text
Other regression checks:
4 / 4 stable across 10 runs
```

### Interpretation

The AI001 golden response itself is deterministic and factually correct.

A direct evaluation of the same response successfully produced:

```text
Overall score:       1.0
Semantic score:      1.0
Rule-based score:    1.0
Passed:              True
```

However, the semantic judge intermittently returned a failing result during repeated test-suite execution.

Therefore, the observed AI001 issue is classified as:

```text
Evaluator / semantic-judge variance
```

rather than a demonstrated regression in the golden response.

### Important Reliability Principle

Automatic retries were not used to hide the intermittent behavior.

The failure was preserved as evidence for reliability and RCA analysis.

---

## 17. Concurrency Testing

Concurrent AI requests were tested using multiple simultaneous requests to Ollama.

### Test Configuration

```text
Concurrent requests: 5
```

### Result

```text
Successful requests: 5
Failed requests:     0
```

The concurrency test completed successfully without observed request failures.

### Test Command

```powershell
pytest tests/concurrency -v
```

---

## 18. Performance Testing

Performance testing was performed at increasing concurrency levels.

The tested concurrency levels were:

```text
1
3
5
10
```

The framework records:

- Average latency
- P50 latency
- P95 latency
- Error rate
- Wall-clock execution time
- Resource samples

### Latest Results

| Concurrency | Avg | P50 | P95 | Wall Time | Errors |
|---:|---:|---:|---:|---:|---:|
| 1 | 10.77s | 10.77s | 10.77s | 11.14s | 0% |
| 3 | 4.31s | 4.32s | 5.42s | 6.00s | 0% |
| 5 | 5.13s | 4.97s | 7.16s | 8.04s | 0% |
| 10 | 8.10s | 8.30s | 12.46s | 14.06s | 0% |

### Interpretation

The tested configuration showed increasing latency at higher concurrency, particularly at concurrency 10.

No breaking point was observed within the tested range of 1–10 concurrent requests.

The concurrency-1 latency is treated as a warm-up/variability observation rather than as evidence of a monotonic latency relationship.

### Performance Command

```powershell
pytest tests/performance -v
```

---

## 19. Resource Telemetry

The performance test samples Docker resource usage while the load test executes.

The telemetry captures:

- CPU percentage
- Memory usage
- Memory percentage
- Number of collected samples

The telemetry currently covers the:

```text
open-webui
```

Docker container.

### Limitation

The performance benchmark sends AI requests directly to Ollama.

Therefore, the collected Open WebUI container telemetry does not represent complete resource consumption of the Ollama/model process.

Host-level and GPU-level resource telemetry was not captured in this benchmark.

This is documented as a coverage limitation rather than being represented as complete resource observability.

---

## 20. Persistent Storage and Restart Recovery

The Open WebUI deployment uses a persistent Docker volume mounted at:

```text
/app/backend/data
```

Container restart recovery was tested.

### Recovery Validation

After restarting the Open WebUI container:

- The container returned to a healthy state.
- The application became available.
- `/api/version` returned HTTP 200.
- Version `0.11.4` was returned.

### Limitation

Individual authenticated user/chat records could not be directly validated because valid QA credentials were unavailable.

Therefore, this area is classified as:

```text
Partial coverage
```

rather than full authenticated persistence validation.

---

## 21. Security and Privacy Testing

The security-focused coverage includes:

- Unauthorized access
- Authentication requirements
- Invalid authentication
- Protected API access
- Prompt-injection scenarios
- Requests for secrets or credentials
- Safety-sensitive prompts
- Potential sensitive-information exposure

Examples in the AI dataset include requests involving:

- System/developer instructions
- Fake system messages
- API keys
- Passwords
- Tokens
- Credential bypass
- Phishing
- Dangerous instructions

The security and safety tests focus on observable application/AI behavior and do not claim to constitute a complete security penetration test.

---

## 22. Safety Testing

The AI dataset includes safety-sensitive scenarios covering:

- Dangerous requests
- Credential bypass
- Phishing
- Secret exposure
- Prompt injection
- System prompt extraction

The evaluator checks for appropriate refusal or safe handling where the scenario requires it.

Safety failures are reported separately from ordinary semantic quality failures.

---

## 23. Prompt Injection Testing

Prompt-injection scenarios include attempts to:

- Reveal hidden system instructions
- Reveal developer instructions
- Reveal chain-of-thought
- Override previous instructions
- Introduce fake system messages
- Request secrets and credentials

These cases are included in the main AI scenario dataset.

---

## 24. CI/CD Quality Gate

GitHub Actions is used to execute automated quality checks.

The CI pipeline runs the project's test suite and acts as a quality gate.

The project also includes a deliberate CI regression demonstration.

### Deliberate Regression

The quality-gate assertion was intentionally changed from:

```python
assert result["passed"] is True
```

to:

```python
assert result["passed"] is False
```

This intentionally caused the CI quality gate to fail.

The failure demonstrated that the pipeline correctly detects a regression.

The assertion was then restored:

```python
assert result["passed"] is True
```

The corrected implementation passed the quality gate.

### Quality Gate Principle

The CI pipeline should fail when required quality checks fail rather than silently accepting a degraded result.

---

## 25. Root-Cause Analysis

Observed failures were classified according to their most likely quality category.

The RCA report is available at:

```text
docs/rca-report.md
```

### RCA Categories

The project distinguishes between:

- AI/application behavior
- Evaluator/judge variance
- Dependency/runtime behavior
- Environment limitations
- Test defects
- Infrastructure failures

### Key RCA Cases

#### AI020 — Secret Exposure Handling

Classified as an AI/application behavior issue based on the observed evaluation behavior.

#### AI015 — Contradictory Instruction Handling

Classified as an AI/application behavior issue involving conflicting instructions.

#### AI008 — Long-Output Timeout

Classified as dependency/runtime behavior because the long-output scenario exceeded the configured execution timeout.

#### AI001 — Golden Evaluation Flakiness

Classified as semantic evaluator/judge variance.

Evidence:

```text
10 reliability runs
3 AI001 failures
7 successful runs
0 retries
```

The same golden response can receive a passing score of `1.0` during another evaluation.

#### Authenticated API Test

Classified as an environment limitation because valid QA credentials were unavailable.

---

## 26. Coverage Matrix

The complete coverage matrix is available at:

```text
docs/coverage-matrix.md
```

The matrix maps assignment requirements to:

- Test implementation
- Test location
- Execution evidence
- Current status
- Known limitations

Major covered areas include:

- Application selection
- Architecture
- Critical workflows
- UI/E2E
- Cross-browser
- API
- Authentication
- Dependency failures
- AI evaluation
- Safety
- Prompt injection
- Golden regression
- Nondeterminism
- Reliability
- Concurrency
- Performance
- CI/CD
- RCA
- Security/privacy
- Persistence
- Resource telemetry

---

## 27. Reports

The project stores machine-readable test results under:

```text
reports/
```

Important reports include:

```text
reports/ai_scenario_results.json
reports/nondeterminism_results.json
reports/reliability_results.json
reports/performance_results.json
reports/quality_baseline.json
```

Documentation reports include:

```text
docs/application-selection.md
docs/architecture.md
docs/critical-workflows.md
docs/test-strategy.md
docs/coverage-matrix.md
docs/rca-report.md
docs/ai-usage-disclosure.md
```

---

## 28. Installation

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Install Playwright browsers:

```powershell
playwright install chromium
playwright install firefox
```

Verify pytest:

```powershell
pytest --version
```

---

## 29. Running the Test Suites

### Run the Complete Pytest Suite

```powershell
pytest -v
```

### Run UI Tests

```powershell
pytest tests/ui -v
```

### Run API Tests

```powershell
pytest tests/api -v
```

### Run Integration Tests

```powershell
pytest tests/integration -v
```

### Run Dependency Failure Tests

```powershell
pytest tests/integration/test_dependency_failures.py -v
```

### Run Concurrency Tests

```powershell
pytest tests/concurrency -v
```

### Run Performance Tests

```powershell
pytest tests/performance -v
```

### Run AI Regression Tests

```powershell
pytest tests/regression/test_ai_regression.py -v
```

### Run Reliability Experiment

```powershell
python tests/regression/run_reliability.py
```

---

## 30. AI Evaluation

The complete AI scenario evaluation can be executed using the evaluation runner.

The evaluation framework loads scenarios from:

```text
datasets/ai_scenarios.json
```

and evaluates responses using the configured evaluation methods.

The resulting report is stored under:

```text
reports/
```

The evaluation framework distinguishes deterministic checks from semantic judge evaluation.

---

## 31. Configuration

The pytest configuration is stored in:

```text
pytest.ini
```

Current configuration includes:

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = -v
markers =
    integration: tests that require external/local services such as Ollama
```

---

## 32. Known Environment Limitations

### Authentication

The local environment did not provide valid QA credentials for an authenticated Open WebUI user.

Therefore, positive authenticated workflows could not be reliably executed.

Unauthenticated authorization behavior was still tested.

### OpenAPI

The `/openapi.json` endpoint returned frontend HTML rather than an OpenAPI specification.

Therefore, no contract tests were created against that response.

### Real-Time E2E

Authenticated streaming/real-time workflows could not be fully exercised because they depend on the unavailable authenticated application path.

### Resource Telemetry

The performance tests capture:

- Request latency
- P50
- P95
- Error rate
- Concurrency behavior
- Docker container CPU/memory samples

However, AI benchmark requests are sent directly to Ollama.

Therefore, Open WebUI container telemetry does not represent complete Ollama/model resource consumption.

### Persistent Storage

Container restart recovery was validated using the persistent Docker volume.

However, individual authenticated user/chat record persistence was not directly validated because valid QA credentials were unavailable.

### Semantic Judge Variance

Semantic AI evaluation is inherently more variable than deterministic checks.

The AI001 reliability experiment demonstrated intermittent judge variance.

This behavior is reported rather than hidden using automatic retries.

---

## 33. Quality Findings

The testing performed in this project produced several important observations.

### Finding 1 — Cross-Browser UI Behavior

The tested unauthenticated and invalid-login workflows passed in both Chromium and Firefox.

```text
4 / 4 UI tests passed
```

### Finding 2 — Dependency Failure Handling

The framework successfully exercised seven dependency failure modes.

```text
7 / 7 dependency tests passed
```

### Finding 3 — AI Evaluation Variability

The AI baseline showed both successful and unsuccessful scenario evaluations.

The reliability experiment demonstrated that AI001 can intermittently fail semantic evaluation despite the golden response being correct.

### Finding 4 — Performance Degradation

Latency increased at higher tested concurrency levels, particularly at concurrency 10.

No breaking point was observed within the tested range.

### Finding 5 — CI Quality Gate

A deliberately introduced regression caused the CI quality gate to fail, demonstrating that the pipeline can detect quality degradation.

### Finding 6 — Authentication Environment Limitation

Authenticated positive workflows could not be validated because valid QA credentials were unavailable.

This limitation is explicitly reported instead of being hidden or bypassed.

---

## 34. Definition of Done Status

The project addresses the major required areas of the assignment.

| Area | Status |
|---|---|
| Application selection | Completed |
| Architecture documentation | Completed |
| Critical workflows | Completed |
| UI/E2E automation | Completed |
| Cross-browser testing | Completed |
| API testing | Completed |
| Authentication testing | Partial |
| Dependency failures | Completed |
| AI scenario dataset | Completed |
| 30+ AI scenarios | Completed |
| Golden dataset | Completed |
| Semantic judge | Completed |
| Judge validation | Completed |
| AI safety testing | Completed |
| Prompt injection | Completed |
| Nondeterminism | Completed |
| Golden regression | Completed |
| Reliability testing | Completed |
| Flakiness analysis | Completed |
| Concurrency testing | Completed |
| Performance testing | Completed |
| Resource telemetry | Partial |
| Persistent storage | Partial |
| Real-time authenticated E2E | Limited |
| CI/CD | Completed |
| CI regression demonstration | Completed |
| RCA | Completed |
| Coverage matrix | Completed |
| Security/privacy coverage | Completed |
| AI usage disclosure | Completed |

---

## 35. AI-Assisted Development Disclosure

AI-assisted tools were used during development to support:

- Test planning
- Test scenario design
- Framework scaffolding
- Debugging
- Failure analysis
- Documentation
- AI evaluation design
- RCA organization

AI assistance was treated as a development aid rather than as evidence.

The project author remained responsible for:

- Application selection
- Environment setup
- Implementation
- Test execution
- Reviewing failures
- Validating fixes
- Interpreting results
- Root-cause classification
- Final documentation

The detailed disclosure is available at:

```text
docs/ai-usage-disclosure.md
```

---

## 36. Reproducibility

The reported results are based on actual executions in the configured local environment.

Where behavior was intermittent, the observed variability is reported rather than hidden.

In particular:

```text
AI001 semantic evaluation
```

was observed to pass and fail across repeated executions.

No automatic retry was used to convert an intermittent failure into a passing result.

This preserves the evidence needed for reliability and RCA analysis.

---

## 37. Final Test Evidence

The most important validated results include:

```text
UI:
4 passed

Dependency failures:
7 passed

Ollama integration:
4 passed

Concurrency:
5/5 successful requests

Nondeterminism:
30/30 stable executions

AI regression:
5 tests capable of passing
with AI001 demonstrating intermittent judge variance

Reliability:
10 runs
7 passed
3 failed
0 retries

Performance:
1, 3, 5, and 10 concurrency levels tested
0% request errors observed
```

---

## 38. Project Goal

The goal of this framework is not simply to produce a collection of passing tests.

It is designed to provide evidence about:

- What works
- What fails
- What is nondeterministic
- What is caused by the AI system
- What is caused by the evaluator
- What is caused by infrastructure or environment limitations
- Where performance degrades
- Where additional test coverage is required

The framework therefore combines conventional automation with AI-specific evaluation and reliability analysis to provide a more complete quality assessment of an AI application.
