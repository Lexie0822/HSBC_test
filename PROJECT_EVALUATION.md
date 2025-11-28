# Project Evaluation and Reflections

This document provides a candid assessment of the **Property Portal** solution relative to the interview specification.  It highlights what has been delivered, discusses design decisions, and offers constructive suggestions for future improvement.  Citations refer back to the task brief for reference.

## Overview of Requirements

The interview asked for three core deliverables:

1. **Housing Price Prediction API** – a FastAPI service exposing `/predict`, `/model‑info` and `/health` endpoints running on Python 3.12+ with a scikit‑learn model【679433521279386†L18-L34】.
2. **Next.js Portal** – a unified portal using the App Router with two applications: a *property value estimator* backed by the Python API and a *property market analysis* app backed by a Java service.  The portal should implement a shared layout, client‑side validation, history and comparison views for the estimator, and interactive dashboards with filters and export options for the analysis【679433521279386†L50-L82】.
3. **System Architecture Design** – a diagram and short write‑up describing a scalable, resilient and cost‑effective cloud solution【679433521279386†L140-L147】.

## Assessment of Task 1: Housing Price Prediction API

**What was done well**

* **Clear model pipeline:** A training script reads the provided CSV, drops non‑feature columns, standardises the features and trains a linear regression model via a `Pipeline`.  The code persists both the model and metadata (coefficients, intercept and evaluation metrics) so that the serving layer can remain stateless and rely on file‑based artefacts.  Saving metrics such as R² (~0.98) and MAE (≈ $7.9k) gives the interviewer an at‑a‑glance sense of performance.
* **FastAPI service:** The API defines three endpoints exactly as specified – `GET /health` returns a simple status, `GET /model‑info` returns the persisted metadata, and `POST /predict` accepts either a single input or a batch and returns an array of prices.  Pydantic models enforce schema validation on inputs, and error conditions are handled via HTTP exceptions.  The API is containerised with a concise `Dockerfile` and documented in the project README.
* **Strong typing and validation:** Using `confloat` and `conint` from Pydantic to restrict ranges (e.g. positive values for square footage, 0–10 for school rating) prevents invalid requests from propagating to the model.  This approach aligns with the brief’s emphasis on handling both single and batch predictions【679433521279386†L26-L34】.

**Potential improvements**

* **Model sophistication:** A linear regression performs adequately on the synthetic dataset but lacks the capacity to capture non‑linear relationships.  Exploring tree‑based models (e.g. random forests or gradient boosting) or regularised linear models might improve generalisation, especially if the dataset exhibits heteroscedasticity.  Cross‑validation and hyper‑parameter tuning (e.g. via `GridSearchCV`) could provide more robust metrics for the `model‑info` endpoint.
* **Feature engineering:** Currently, the service assumes all raw features are numeric and equally informative.  Incorporating domain knowledge—such as one‑hot encoding for discrete variables (bedroom count), interaction terms (lot size × distance to city centre) or log‑transformations for skewed distributions—could reduce model bias.  Additionally, including macroeconomic indicators (interest rates, regional growth indices) would make the estimator more realistic.
* **Asynchronous design and performance:** The API loads the model at startup, but calls to the model run synchronously in the request thread.  For high concurrency, one might offload predictions to a background worker, use shared memory for the model or expose predictions via a queue.  Returning a job ID and allowing the client to poll for results would improve scalability.
* **Security and observability:** The current implementation lacks authentication, rate limiting or logging.  In production, exposing an unauthenticated prediction endpoint could lead to misuse.  Integrating OpenTelemetry for tracing, structured logging and metrics would satisfy real‑world readiness.

## Assessment of Task 2: Multi‑Application Next.js Portal

**What was done well**

* **Unified App Router:** The portal uses Next.js App Router with a shared layout.  Navigation links to the *Property Value Estimator* and *Property Market Analysis* are consistent across pages.  Tailwind CSS provides a clean baseline style and responsive grid layouts.
* **Working estimator form:** The estimator page contains a form that mirrors the features used for training.  On submission it calls the FastAPI service and displays the predicted price.  Basic error handling informs the user if the request fails.  While minimal, this meets the core requirement of interacting with the ML model【679433521279386†L64-L75】.
* **Minimal analysis dashboard:** The analysis page fetches aggregate statistics from the Spring Boot service and displays count, average, minimum and maximum prices.  The Java backend pre‑computes these values at startup, reducing latency and satisfying the core requirement to expose aggregate stats【679433521279386†L83-L86】.

**Areas lacking and suggestions**

* **Client‑side validation and user experience:** The form enforces required fields but does not display contextual validation errors (e.g. invalid ranges) until after submission.  Implementing custom hooks with `react‑hook‑form` or Zod could provide per‑field error messages and client‑side constraints before hitting the API.  Additionally, the UI could visualise predictions with charts and summarise the history of previous estimates per user.
* **History and comparison:** The brief calls for a history feature and a comparison view to analyse multiple properties side‑by‑side【679433521279386†L68-L71】.  This skeleton lacks state management beyond the local component; adding a global store (e.g. Context API, Zustand or Redux) would allow persisting estimates across page visits.  A table component with selectable rows could facilitate side‑by‑side comparison of predicted prices.
* **Property market dashboard:** The analysis app was intended to include interactive visualisations, filters by property segment and “what‑if” analysis based on the model【679433521279386†L77-L80】.  The current implementation exposes only four aggregate statistics.  A richer dashboard could use charts (e.g. via recharts or Chart.js) to show price distributions, scatter plots of price vs. square footage, and histograms of year built.  Filters for ranges and categories would enable deeper exploration, while export buttons (CSV, PDF) would satisfy the requirement for data export【679433521279386†L77-L81】.
* **Backend integration:** The portal currently calls the Python and Java services directly from the client.  In production this requires CORS configuration and separate network endpoints.  A more robust pattern would introduce a Next.js API route acting as a proxy, centralising authentication, caching and error handling.  Using `SWR` or `React Query` for data fetching would provide automatic caching and revalidation.
* **Accessibility and polish:** To meet the WCAG guidelines mentioned in the brief【679433521279386†L97-L99】, inputs and buttons should have ARIA labels, semantic HTML and keyboard focus states.  Animations and loading skeletons could improve perceived performance when waiting for predictions or statistics.  Form inputs could use sliders or steppers for values like school rating to enhance usability.

## Assessment of Task 3: System Architecture Design

* **Deliverables produced:** A simple architecture diagram illustrates how the Next.js portal communicates with two containerised backends (Python and Java) through REST, with object storage for the model artefacts and a managed database layer.  The accompanying document explains infrastructure choices, including container orchestration, auto‑scaling groups, object storage for datasets and artefacts, and a CI/CD pipeline using GitHub Actions.  This satisfies the requirement for a diagram and brief explanation【679433521279386†L140-L147】.
* **Opportunities for elaboration:** The design could delve deeper into resilience and cost optimisation.  For example, using managed Kubernetes (e.g. AWS EKS or GKE) with horizontal pod auto‑scalers ensures the services scale under load.  Front‑end assets could be served via a CDN (e.g. CloudFront) with edge caching.  A message queue (Kafka or AWS SQS) could decouple user requests from long‑running predictions, and a Redis cache could store frequently requested statistics.  Observability could be improved by integrating metrics and tracing pipelines (Prometheus, Grafana, ELK stack).  CI/CD might include static analysis, unit and integration tests, vulnerability scanning and deployment to staging environments before production promotion.

## Final Thoughts and Next Steps

Overall, the submitted project demonstrates the ability to build a full‑stack solution across Python, Java and React ecosystems within a limited timeframe.  The core endpoints work as intended, the services are containerised, and the portal stitches them together.  The architecture document shows awareness of cloud best practices.

However, to take this from a minimal proof‑of‑concept to a production‑ready system, further investment is needed.  Richer frontend features (history, comparisons, dashboards), robust validation, security, logging and monitoring are essential.  On the modelling side, exploring more expressive algorithms and feature engineering would improve predictive accuracy and fairness.  Architecturally, adding caching, asynchronous processing and auto‑scaling would ensure the platform scales with demand and remains cost‑efficient.

These reflections are intended to demonstrate not only what was delivered but also a critical thought process about how to improve and extend the system in real‑world scenarios.