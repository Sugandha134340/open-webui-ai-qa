# Application Selection and Analysis

## 1. Selected Application

The selected application for this QA automation project is **Open WebUI v0.11.4**, an open-source web interface for interacting with AI/LLM backends.

The application was selected because it provides a realistic AI-powered workflow that allows testing across multiple QA dimensions, including:

- UI and end-to-end workflows
- API and backend behavior
- authentication and authorization
- AI/LLM response quality
- dependency failures
- concurrency
- performance and latency
- safety and prompt-injection behavior
- reliability and nondeterminism
- CI/CD quality gates

The selected version was pinned to **Open WebUI v0.11.4** to make the test environment reproducible.

---

## 2. Selection Rationale

The application was evaluated against the requirements of the assignment.

| Evaluation Area | Open WebUI Coverage |
|---|---|
| AI-powered functionality | Yes |
| Web UI | Yes |
| Backend/API layer | Yes |
| External AI dependency | Yes — Ollama |
| AI response evaluation | Yes |
| Authentication | Yes |
| Negative/edge-case testing | Yes |
| Dependency failure testing | Yes |
| Concurrency testing | Yes |
| Performance testing | Yes |
| Safety testing | Yes |
| Non-deterministic AI behavior | Yes |
| CI/CD integration | Yes |
| Real-time/streaming behavior | Available, but authenticated E2E was limited by the local environment |

The application therefore provides a suitable environment for demonstrating evidence-driven AI quality engineering rather than only conventional UI automation.

---

## 3. Version and Environment

The application was deployed using Docker with the following image:

```text
ghcr.io/open-webui/open-webui:v0.11.4
```

The application was exposed locally through:

```text
http://localhost:3000
```

The deployed application version was verified through:

```text
/api/version
```

with the response:

```json
{
  "version": "0.11.4",
  "deployment_id": ""
}
```

The AI backend used for the evaluation environment was **Ollama**, with the `llama3.2:3b` model available.

---

## 4. High-Level Architecture

The tested environment consists of the following major components:

```text
                    Browser
                       |
                       v
              +----------------+
              |   Open WebUI   |
              |    v0.11.4     |
              +----------------+
                       |
                       v
                  Ollama API
                       |
                       v
                 llama3.2:3b
```

The QA framework interacts with the system through multiple layers:

```text
                    QA Framework
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
        UI Tests      API Tests      AI Tests
          |              |              |
          +--------------+--------------+
                         |
                         v
                  Open WebUI / Ollama
```

---

## 5. QA Architecture Around the Application

The automation framework was designed to test different layers independently while also supporting end-to-end validation.

```text
                    Test Framework
                          |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
   UI / E2E            API / Backend      AI Evaluation
       |                  |                  |
       v                  v                  v
  Playwright          HTTP Requests      Ollama Client
       |                  |                  |
       +------------------+------------------+
                          |
                          v
                   Evidence / Reports
```

The AI evaluation layer additionally contains:

```text
AI Scenario Dataset
        |
        v
Scenario Runner
        |
        v
AI Response
        |
        +-------------------+
        |                   |
        v                   v
Rule-Based Evaluator   Semantic Evaluator
        |                   |
        +---------+---------+
                  |
                  v
          Evaluation Result
```

---

## 6. Critical Dependencies

The main dependency relationships identified during testing are:

| Component | Role |
|---|---|
| Open WebUI | Application under test |
| Ollama | AI model backend |
| `llama3.2:3b` | Local language model |
| Docker | Application runtime |
| Playwright | Browser automation |
| Pytest | Test execution |
| GitHub Actions | CI/CD quality gate |

The dependency relationship is important for failure-injection testing because AI behavior depends on an external model-serving component.

---

## 7. Why This Application Is Suitable for AI QA

A conventional CRUD application would not adequately demonstrate the AI-specific requirements of the assignment.

Open WebUI provides observable AI behavior that can be evaluated for:

- correctness
- relevance
- consistency
- groundedness
- instruction following
- safety
- prompt-injection resistance
- hallucination behavior
- latency
- nondeterminism
- failure handling

The application therefore supports the central objective of the project: building quality infrastructure that can distinguish ordinary application failures from AI-quality issues and test/evaluation instability.

---

## 8. Scope and Environment Limitations

The local environment introduced several limitations that are documented rather than treated as successful coverage.

### Authentication

Valid QA credentials for an authenticated Open WebUI user were not available.

Therefore:

- unauthenticated authorization behavior was tested;
- invalid credential handling was tested;
- positive authenticated workflows could not be reliably executed.

### Real-Time E2E

Open WebUI supports streaming AI responses, but the authenticated application path was unavailable in the local environment.

Therefore, full authenticated streaming failure/recovery testing could not be completed.

Additional AI evaluation was used to increase coverage of the AI-specific requirements.

### OpenAPI

The `/openapi.json` endpoint was investigated, but the response was frontend HTML rather than a valid OpenAPI specification.

Therefore, contract tests were not created against an unavailable/invalid API schema.

### Resource Telemetry

Performance testing includes Docker container resource sampling for Open WebUI.

The AI benchmark itself sends requests directly to Ollama, so the collected Open WebUI container telemetry does not represent complete Ollama/model-process resource usage.

---

## 9. Selection Conclusion

Open WebUI v0.11.4 provides a realistic AI-powered system with sufficient observable behavior to exercise the required QA dimensions.

The project therefore focuses on building reusable, evidence-driven automation around:

```text
UI
API / Backend
AI / LLM Evaluation
Dependency Failures
Safety
Nondeterminism
Reliability
Concurrency
Performance
CI/CD
Root-Cause Analysis
```

The documented environment limitations are incorporated into the coverage matrix and final test reports rather than being hidden.