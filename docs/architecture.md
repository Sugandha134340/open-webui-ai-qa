# Open WebUI QA Architecture

## 1. System Under Test

The system under test is Open WebUI v0.11.4 running as a Docker container.

```text
Application:
Open WebUI

Docker image:
ghcr.io/open-webui/open-webui:v0.11.4

Container:
open-webui

Application port:
3000 (host) -> 8080 (container)

AI provider:
Ollama

Model:
llama3.2:3b

Persistent volume:
open-webui
```

The Docker image reports the following build version:

```text
8bd8b4fac5e059578ac0c74b3c18d11139f88b7d
```

This version is recorded so that test results can be associated with a specific application build.

---

## 2. High-Level Architecture

The current test environment can be represented as:

```text
                         QA Framework
                              |
                +-------------+-------------+
                |             |             |
              UI Tests     API Tests    AI Evaluators
                |             |             |
                +-------------+-------------+
                              |
                              v
                    +-------------------+
                    |    Open WebUI      |
                    |      v0.11.4       |
                    |   Docker container |
                    +---------+---------+
                              |
                       AI provider path
                              |
                              v
                    +-------------------+
                    |      Ollama        |
                    |    llama3.2:3b     |
                    +-------------------+

                              |
                              v
                    +-------------------+
                    | Persistent Data   |
                    | Docker Volume     |
                    |   open-webui      |
                    +-------------------+
```

The QA framework will interact with Open WebUI through multiple observable layers rather than testing only the browser interface.

---

## 3. Runtime Environment

The application is deployed using Docker.

The container exposes:

```text
Host:      localhost:3000
Container: 8080
```

The container configuration also includes:

```text
DOCKER=true
ENV=prod
PORT=8080
```

The Docker environment contains configuration for:

```text
Ollama
OpenAI-compatible providers
RAG embeddings
Whisper
Tiktoken
```

The current test environment primarily uses Ollama with a local language model.

---

## 4. Persistent Storage

The application uses a Docker volume named:

```text
open-webui
```

The volume is mounted into the application at:

```text
/app/backend/data
```

This provides persistent application data across container recreation.

The QA framework will use this persistence layer to test:

* Chat persistence
* Conversation retrieval
* State consistency
* Data isolation
* Behavior after application restart
* Cleanup between tests where required

Tests must avoid relying on undocumented pre-existing user data.

---

## 5. Backend/API Layer

The running application's logs demonstrate active HTTP API traffic.

Examples observed during normal application use include:

```text
GET /api/version
GET /api/v1/chats/
GET /api/v1/chats/pinned
GET /api/v1/folders/
GET /api/v1/folders/shared
GET /_app/version.json
```

These endpoints provide observable backend behavior that can be exercised independently of the browser.

The API testing layer will therefore validate:

* HTTP status codes
* Response structures
* Authentication
* Authorization
* Invalid requests
* Error handling
* State changes
* Persistence
* Duplicate requests
* Failure recovery

API tests will be preferred over UI interaction when the behavior can be tested more deterministically at the backend layer.

---

## 6. AI Provider Layer

The current environment uses Ollama as the local AI provider.

The intended logical flow is:

```text
User
  |
  v
Open WebUI
  |
  v
AI provider integration
  |
  v
Ollama
  |
  v
llama3.2:3b
  |
  v
Generated response
  |
  v
Open WebUI
  |
  v
User
```

The AI provider is treated as a dependency rather than as part of the core Open WebUI implementation.

This allows the QA framework to distinguish:

```text
Open WebUI defect
        vs
AI/model variability
        vs
Ollama dependency failure
        vs
Test/infrastructure failure
```

The exact network interaction between the Open WebUI container and Ollama will be verified as part of dependency and integration testing rather than assumed from configuration alone.

---

## 7. AI Evaluation Layer

AI evaluation is a separate layer from functional API/UI assertions.

The evaluator will inspect observable AI behavior.

The initial evaluation dimensions are:

### Correctness

Whether the response satisfies the expected answer or task.

### Relevance

Whether the response addresses the user's request without unnecessary unrelated content.

### Completeness

Whether important required information is present.

### Consistency

Whether repeated executions of the same scenario remain within the accepted tolerance.

### Groundedness

For RAG/knowledge workflows, whether the response is supported by the retrieved information.

### Safety

Whether the system follows defined safety and access constraints.

### Tool behavior

Where tools are involved:

* Correct tool selected
* Correct parameters
* Correct ordering
* No unnecessary calls
* No duplicate calls
* Correct failure handling

### Latency

AI latency will be recorded separately from ordinary application/API latency.

---

## 8. Test Architecture

The QA framework is organized into independent layers.

```text
open-webui-ai-qa/
│
├── tests/
│   ├── ui/
│   ├── api/
│   ├── e2e/
│   ├── ai/
│   ├── integration/
│   ├── concurrency/
│   └── performance/
│
├── framework/
│   ├── clients/
│   ├── data/
│   ├── evaluators/
│   ├── fixtures/
│   └── utils/
│
├── datasets/
│   ├── ai_scenarios.json
│   └── golden_dataset.json
│
└── reports/
```

### UI

Responsible for browser-level workflows using Playwright.

### API clients

Responsible for communicating with Open WebUI APIs directly.

### Fixtures

Responsible for:

* Test users
* Authentication
* Test data
* Application state
* Cleanup
* Environment configuration

### Evaluators

Responsible for AI-specific evaluation.

### Data

Contains deterministic synthetic test data and scenario definitions.

### Integration

Tests interactions between Open WebUI and external dependencies such as Ollama.

### Concurrency

Tests race conditions and concurrent operations.

### Performance

Measures API and AI-path performance under increasing load.

---

## 9. Multi-Layer Test Flow

A complete critical workflow will be tested across multiple layers.

Example:

```text
             UI / Playwright
                    |
                    v
             Open WebUI UI
                    |
                    v
              Backend API
                    |
                    v
             AI Provider
                    |
                    v
                Ollama
                    |
                    v
              llama3.2:3b
                    |
                    v
              AI Response
                    |
          +---------+---------+
          |                   |
       UI check          AI evaluator
          |                   |
          +---------+---------+
                    |
                    v
              Test Result
```

This allows a failure to be localized more precisely.

For example:

```text
UI failure
    -> inspect API

API successful
    -> inspect AI response

AI response incorrect
    -> inspect model/provider

Provider unavailable
    -> classify as dependency failure
```

---

## 10. Dependency Failure Architecture

The QA framework will deliberately test AI dependency failures.

The target scenarios include:

```text
Normal
  |
  +--> Ollama unavailable
  |
  +--> Ollama timeout
  |
  +--> Slow Ollama response
  |
  +--> Invalid/malformed response
  |
  +--> Partial dependency failure
  |
  +--> Recovery
```

Expected behavior will include:

* Safe failure
* Useful user-facing error
* No corrupted conversation state
* No unintended duplicate operation
* Appropriate retry behavior where applicable
* Recovery after dependency restoration

---

## 11. AI Nondeterminism Architecture

AI responses are not expected to be identical for every execution.

Therefore:

```text
Scenario
   |
   +--> Run 1
   +--> Run 2
   +--> Run 3
   +--> ...
   +--> Run N
           |
           v
    Evaluation metrics
           |
           v
    Tolerance analysis
```

The framework will distinguish:

### Expected variance

Different wording but equivalent task success.

### Acceptable variance

Small evaluator-score or latency variation within defined thresholds.

### AI quality regression

A meaningful deterioration in correctness, safety, tool behavior, or another defined quality dimension.

### Infrastructure failure

The application or test environment failed before meaningful AI evaluation could occur.

This prevents ordinary model variability from being incorrectly reported as a product regression.

---

## 12. Observability and Evidence

Every important test result should contain enough information to reproduce and diagnose the failure.

Evidence may include:

* Scenario ID
* Test name
* Timestamp
* Application version
* Model
* Environment
* Request
* Response
* HTTP status
* Tool calls
* AI evaluation result
* Latency
* Error information
* Screenshot for UI failures
* Relevant application logs

The framework will use structured reports rather than relying only on console output.

---

## 13. Quality-Gate Architecture

The eventual CI pipeline will classify test results into blocking and non-blocking conditions.

```text
                         CI Pipeline
                              |
                  +-----------+-----------+
                  |                       |
             Blocking                Warning
                  |                       |
        Critical regression        Minor variance
        API contract failure       Flaky test
        Severe AI regression       Performance warning
        Safety failure
                  |
                  v
             Build blocked
```

The goal is to make the quality infrastructure enforceable rather than simply generating reports.

---

## 14. Architecture Testing Priorities

The initial implementation will prioritize:

1. Critical AI workflows
2. API/backend validation
3. UI/E2E coverage
4. AI evaluation
5. Dependency failure handling
6. Non-deterministic evaluation
7. Golden regression testing
8. Safety/adversarial testing
9. Reliability and flakiness
10. Concurrency
11. Performance and AI latency
12. CI quality gates
13. Root-cause analysis
14. Security/privacy validation

The project will prioritize meaningful quality signals over a large number of shallow tests.
