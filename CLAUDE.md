---
description: Global coding standards for this multi-deliverable Python API project
alwaysApply: true
---

# Global Development Rules

## Communication

- Keep responses very short.
- Use a professional tone.
- Do not explain unless explicitly requested.

## Scope and Priority

- Apply these rules by default across the workspace.
- If an activity/instruction requires specific names or structure, follow the activity/instruction first.

## Project Context

- Multi-deliverable project building a task management API with AI integrations.
- Entregable 1: REST API with JSON file persistence.
- Entregable 2: AI-powered endpoints (LLM integration via Azure OpenAI or Anthropic).
- Entregable 3: Jinja UI + MySQL database via SQLAlchemy.
- Entregables 4–5: Docker, CI/CD pipelines, and Azure cloud deployment.
- Multi-agent workflow: agents defined in `.agents/`, plans in `plans/`, prompts in `prompts/`.
- Source code lives under `src/`, tests under `tests/`.

## General Standards

- Preserve backward compatibility unless explicitly requested otherwise.
- Prefer minimal diffs and avoid unrelated changes.
- Do not introduce new dependencies unless necessary.
- Never commit secrets or credentials.
- Store configuration in environment variables; never in source code.
- Provide `.env.example`; add `.env` to `.gitignore`.
- Validate all external inputs.

## Naming and Language

- Use English for file names, function names, class names, variable names, comments, and docstrings.
- Exception: keep required non-English names only when the activity explicitly mandates them.
- Code comments must be brief and descriptive.
- Prefer one-line comments whenever possible.
- Do not add comments that only restate function parameters or return values.

## Python Rules

- Follow PEP8.
- Use 4 spaces for indentation.
- Use type hints in all public functions and methods.
- Use strict typing:
    - Avoid `Any` unless strictly justified.
    - Type all parameters and return values.
- Prefer Pydantic models or `dataclasses` for structured data.
- Keep functions small and single-purpose.
- Avoid global state unless strictly necessary.
- Use Python `logging` (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- Do not silently suppress exceptions; raise actionable errors.
- Public modules, classes, and functions must include docstrings.

## API Design Rules

- All endpoints return JSON responses.
- Use appropriate HTTP status codes (200, 201, 204, 400, 404, 422, 500).
- Validate request data before processing.
- Keep endpoint logic thin; delegate business logic to service/manager classes.
- Prefer auto-generated API documentation when the framework supports it.

## Data Persistence Rules

- Entregable 1: use `tasks.json` for persistence exclusively via `TaskManager`.
- Never read/write the JSON file directly from endpoint handlers.
- From entregable 3 onwards: SQLAlchemy + MySQL; design models to minimise migration effort.

## HTML Rules

- Use semantic HTML5 elements.
- Use 4 spaces for indentation.
- Keep structure readable and consistent.
- Use lowercase tags and attributes.
- Use double quotes for attribute values.
- Add `alt` text for informative images.
- Ensure basic accessibility (`label` for inputs, logical heading order).
- Target WCAG AA minimum for any HTML interface.
- Confirm Bootstrap usage with the user before implementation.

## CSS Rules

- Use 4 spaces for indentation.
- Prefer class-based selectors over ids for styling.
- Avoid `!important` unless strictly necessary.
- Keep selectors simple and maintainable.
- Group related declarations; keep consistent property ordering.
- Prefer responsive layouts and relative units.

## JavaScript Rules

- Use 4 spaces for indentation.
- Use `const` by default; `let` only when reassignment is required; never `var`.
- Use strict equality (`===`, `!==`).
- Keep functions small and single-purpose.
- Use clear, descriptive English names.
- Handle errors explicitly; do not swallow exceptions.
- Avoid implicit globals and side effects.

## Testing Rules

- Framework: `pytest` for Python.
- Minimum test coverage: 80%.
- Tests must be deterministic, isolated, and fast.
- Add/update tests for any new or changed logic.
- Test structure: `tests/test_<module>.py`.

## Documentation Rules

- Keep `README.md` updated when behavior, setup, or usage changes.
- Include objective, installation, execution, and usage examples for deliverables.

## Security Rules

- Never execute arbitrary user-provided code.
- Sanitize/validate input data before processing.
- Keep dependencies updated when modifying the project.
- API keys and credentials go in environment variables only.
