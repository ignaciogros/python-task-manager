# Plan: Entregable 1 — Task Management REST API

## Overall status
- [x] Step 0: Planning
- [x] Step 1: Framework Decision — **FastAPI** ✓
- [x] Step 2: Project Structure Setup ✓
- [x] Step 3: Data Model (`Task`) ✓
- [x] Step 4: Persistence (`TaskManager`) ✓
- [x] Step 5: API Endpoints ✓
- [ ] **Step 6: Review & Validation** ← CURRENT
- [ ] Step 7: Packaging

---

## Step 1: Framework Decision — Flask vs FastAPI ✅ DONE

> **Decision: FastAPI** — confirmed by user.

### Comparison

| Criterion | Flask | FastAPI |
| :--- | :---: | :---: |
| Explicitly named in entregable 1 instructions | ✅ | ❌ |
| Mentioned as valid option in entregable 2–3 | ✅ | ✅ |
| Auto-generated OpenAPI/Swagger UI | ❌ | ✅ |
| Built-in request validation | ❌ (manual) | ✅ (Pydantic) |
| Type hint integration | ❌ minimal | ✅ native |
| Pydantic (required in entregable 3) | ❌ add-on | ✅ built-in |
| Async/await support | ❌ limited | ✅ native |
| Learning curve | ✅ lower | ⚠️ slightly higher |
| Community maturity | ✅ very large | ✅ large, fast-growing |

### Recommendation: **FastAPI**

1. **Pydantic is required in entregable 3.** FastAPI uses it natively; Flask would require a migration later.
2. **Swagger UI out of the box.** Entregable 2 recommends testing with Postman/Swagger — FastAPI provides this for free.
3. **Aligns with coding rules.** Strict type hints are a project standard; FastAPI enforces them at the framework level.
4. **Better fit for LLM integrations.** Async support helps when calling external AI APIs (entregable 2).
5. **Already accepted upstream.** Entregables 2 and 3 instructions explicitly say "Flask o FastAPI".

> Decision confirmed by user on 2026-05-02.

---

## Step 2: Project Structure Setup

- Create `src/entregable1/` with package layout.
- Initialize virtual environment (`python -m venv venv`).
- Create `requirements.txt` with chosen framework + dependencies.
- Create empty `tasks.json`.
- Add `.env.example` and update `.gitignore`.

Acceptance criteria: `uvicorn src.entregable1.main:app` (or equivalent) starts without errors.

---

## Step 3: Data Model — `Task`
*(Unlocked after Step 2)*

- Implement `Task` class/model with fields: `id`, `title`, `description`, `priority`, `effort_hours`, `status`, `assigned_to`.
- Implement `to_dict()` and `from_dict()` methods.
- Write unit tests in `tests/test_task.py`.

Acceptance criteria: all unit tests pass; `from_dict(task.to_dict()) == task`.

---

## Step 4: Persistence — `TaskManager`
*(Unlocked after Step 3)*

- Implement `TaskManager` with static methods `load_tasks()` and `save_tasks()`.
- Handle missing file and malformed JSON gracefully.
- Write unit tests in `tests/test_task_manager.py`.

Acceptance criteria: round-trip save/load preserves all fields; tests pass.

---

## Step 5: API Endpoints
*(Unlocked after Step 4)*

| Method | Endpoint | Status code (success) |
| :--- | :--- | :--- |
| GET | `/tasks` | 200 |
| GET | `/tasks/{id}` | 200 / 404 |
| POST | `/tasks` | 201 |
| PUT | `/tasks/{id}` | 200 / 404 |
| DELETE | `/tasks/{id}` | 204 / 404 |

- Write integration tests in `tests/test_api.py`.

Acceptance criteria: all endpoints return correct status codes and JSON; integration tests pass.

---

## Step 6: Review & Validation
*(Unlocked after Step 5)*

- Run Reviewer agent on all modules.
- Verify test coverage ≥ 80%.
- Confirm `tasks.json` and `.env` are not committed (check `.gitignore`).
- Verify `requirements.txt` is complete and pinned.

Acceptance criteria: no blockers from Reviewer; coverage ≥ 80%.

---

## Step 7: Packaging
*(Unlocked after Step 6)*

- Update `README.md` with setup and run instructions.
- Package project as `m2_proyecto_nombre_apellido.zip`.

Acceptance criteria: zip extracts cleanly; app runs from a fresh install following README.
