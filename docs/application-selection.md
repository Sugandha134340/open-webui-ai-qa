# Application Selection Report

## 1. Selected Application

**Application:** Open WebUI
**Repository:** `open-webui/open-webui`
**Version:** v0.11.4
**Deployment:** Docker
**AI Provider:** Ollama
**Local Model:** `llama3.2:3b`
**Application URL:** `http://localhost:3000`

Open WebUI was selected as the system under test because it is a real, actively developed open-source AI application with substantial application logic and multiple layers that can be tested independently and together.

The application provides a web-based interface for interacting with AI models and supports functionality beyond a simple model wrapper, including conversations, authentication, persistent application data, retrieval-augmented generation (RAG), tools/functions, and integration with different AI providers.

The application is deployed locally using Docker, while the AI model is served locally through Ollama. This provides a reproducible test environment without depending on a personal cloud account or manually maintained application state.

---

## 2. Repository and Version

**Repository:** `https://github.com/open-webui/open-webui`

**Selected version:** `v0.11.4`

The application is executed using the Docker image:

```text
ghcr.io/open-webui/open-webui:v0.11.4
```

The image is pinned to a specific release rather than using the moving `main` tag. This is important for reproducibility because the system under test should not silently change while the QA framework is being developed.

The application data is persisted through the Docker volume:

```text
open-webui:/app/backend/data
```

---

## 3. Purpose of the Application

Open WebUI provides a web interface for interacting with AI models.

Its core workflow allows a user to:

1. Authenticate with the application.
2. Select an available AI model.
3. Submit a prompt.
4. Send the request to the configured AI provider.
5. Receive the generated response.
6. Continue the conversation using previous conversation context.
7. Persist and access conversation data.

The application also provides additional AI-oriented functionality that creates opportunities for deeper quality testing.

---

## 4. AI Functionality

The primary AI functionality is conversational interaction with configured language models.

For this project, Ollama is used as the local model provider with:

```text
Model: llama3.2:3b
```

The QA framework will evaluate observable AI behavior rather than hidden reasoning.

The evaluation will focus on:

* Correctness
* Relevance
* Completeness
* Consistency
* Groundedness where applicable
* Tool-call correctness
* Failure handling
* Safety and constraint adherence
* Latency

For agent/tool workflows, evaluation will focus on the observable trajectory, including:

* Whether the correct tool was selected
* Whether the tool parameters were correct
* Whether tools were unnecessarily called
* Whether duplicate tool calls occurred
* Whether failures were handled correctly
* Whether the final response was consistent with tool results

Hidden chain-of-thought will not be evaluated.

---

## 5. Application Architecture

The selected application contains multiple layers relevant to quality engineering.

### Frontend

The user interacts with Open WebUI through its web frontend.

The frontend is responsible for:

* Authentication flows
* Model selection
* Chat interaction
* Conversation navigation
* File/document interactions
* Tool-related UI
* Displaying generated responses
* Handling asynchronous/streaming interaction

### Backend

The application uses a backend API layer responsible for application logic and communication with external/internal services.

Relevant backend responsibilities include:

* Authentication and authorization
* Chat and conversation operations
* Model/provider integration
* Tool management and execution
* Configuration
* Retrieval-related operations
* Persistent application state

### Persistent Storage

Open WebUI uses persistent application storage for data and configuration.

The Docker deployment persists application data using:

```text
open-webui:/app/backend/data
```

This allows tests to verify state persistence and consistency across application interactions.

### AI Provider

The current test environment uses:

```text
Open WebUI
      |
      v
    Ollama
      |
      v
 llama3.2:3b
```

This separation is particularly useful for dependency-failure testing because the AI provider can be treated as an independently failing dependency.

---

## 6. Authentication and Authorization

Authentication is part of the application and provides an important test surface.

The QA framework will test:

* Login behavior
* Invalid authentication
* Session handling
* Session expiration where reproducible
* Access to protected resources
* User isolation
* Authorization boundaries
* Unauthorized API access

The goal is to verify that authentication and authorization failures do not expose protected application data or allow unauthorized operations.

---

## 7. External and Internal Dependencies

The primary dependencies in the current environment are:

| Dependency         | Purpose             | Failure scenarios                                |
| ------------------ | ------------------- | ------------------------------------------------ |
| Open WebUI         | System under test   | Application unavailable, backend failure         |
| Ollama             | AI model provider   | Timeout, unavailable service, invalid response   |
| `llama3.2:3b`      | Language model      | Slow response, incorrect response, variability   |
| Docker             | Application runtime | Container failure, restart, resource constraints |
| Persistent storage | Application state   | Persistence and consistency failures             |

Additional Open WebUI functionality may introduce other dependencies, particularly when testing RAG, external search, tools, or other integrations.

---

## 8. Critical Workflows

The initial critical workflows selected for this QA project are:

### WF-01 — AI Chat

```text
User
  ↓
Login
  ↓
Open Chat
  ↓
Select Model
  ↓
Submit Prompt
  ↓
Open WebUI Backend
  ↓
Ollama
  ↓
LLM Response
  ↓
Display Response
  ↓
Persist Conversation
```

### WF-02 — Multi-Turn Conversation

```text
Prompt 1
   ↓
AI Response
   ↓
Prompt 2 referencing previous context
   ↓
AI Response
```

The test must verify that the second response correctly uses the relevant conversation context.

### WF-03 — RAG / Knowledge Workflow

```text
Document
   ↓
Upload / Processing
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Storage
   ↓
User Query
   ↓
Retrieval
   ↓
LLM
   ↓
Grounded Response
```

This workflow provides opportunities to test retrieval correctness, groundedness, missing information, contradictory information, and document-processing failures.

### WF-04 — Tool Execution

```text
User Request
   ↓
AI
   ↓
Tool Selection
   ↓
Tool Parameters
   ↓
Tool Execution
   ↓
Tool Result
   ↓
AI Final Response
```

Tests will validate tool selection, parameters, unnecessary calls, duplicate calls, failure handling, and consistency between tool results and the final response.

### WF-05 — AI Dependency Failure

```text
User Request
   ↓
Open WebUI
   ↓
Ollama
   ↓
Dependency Failure
   ↓
Open WebUI Error Handling
   ↓
User
```

The test framework will inject dependency failures such as:

* Service unavailable
* Timeout
* Slow response
* Malformed response
* Authentication failure where applicable
* Partial failure

The expected behavior is safe failure, useful error handling, and preservation of application consistency.

---

## 9. Testability Challenges

The application presents several challenges that make it suitable for an AI quality-engineering assignment.

### AI nondeterminism

The same prompt can potentially produce different valid responses across repeated executions.

Therefore, exact string matching will not be used as the only AI evaluation mechanism.

### AI correctness

A response can be fluent while still being incorrect.

The evaluation framework therefore needs explicit expected behavior and structured evaluators.

### Tool behavior

For tool-enabled workflows, evaluating only the final response is insufficient.

The framework must also inspect observable tool behavior such as tool selection and parameters.

### External dependency failures

The AI provider is an independent service and can fail independently from Open WebUI.

The framework therefore needs dependency-failure testing and service virtualization/mocking where appropriate.

### Asynchronous behavior

AI generation, streaming responses, document processing, and other operations may not complete immediately.

Tests must synchronize against observable application state rather than relying on arbitrary fixed sleeps.

### Flakiness

AI variability and asynchronous application behavior can produce different outcomes.

The project will distinguish:

* Genuine product regression
* Expected AI variance
* Flaky test
* Infrastructure failure
* Test defect

### Reproducibility

The application version and local model provider must remain controlled so that changes in the test environment do not get mistaken for application regressions.

---

## 10. Why Open WebUI Provides Sufficient Testing Depth

Open WebUI provides enough functionality to exercise multiple layers of an AI quality framework.

The project can cover:

* UI/E2E testing
* API/backend testing
* Authentication and authorization
* Persistent state
* AI response evaluation
* Multi-turn conversations
* RAG evaluation
* Tool-call evaluation
* Dependency failure testing
* Async behavior
* Concurrency
* Performance and latency
* AI safety/adversarial scenarios
* Non-deterministic regression
* CI/CD quality gates
* Observability and diagnostics
* Root-cause analysis

This makes it possible to build a quality infrastructure around a real AI application rather than testing an isolated model or a simple API wrapper.

---

## 11. Known Limitations of the Current Setup

The current local environment uses:

```text
Open WebUI v0.11.4
Ollama
llama3.2:3b
```

Therefore, the test results will primarily represent this local configuration.

Results may differ when using:

* Different Open WebUI versions
* Different language models
* Different model sizes
* Cloud AI providers
* Different hardware
* Different model parameters
* External search or integration providers

Where a capability such as real-time communication is not applicable to a particular workflow, the project will substitute deeper AI evaluation, adversarial testing, dependency-failure testing, or stochastic evaluation as appropriate.

---

## 12. Selection Rationale

Open WebUI was selected because it provides a
