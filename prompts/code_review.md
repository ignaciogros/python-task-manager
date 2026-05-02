# Prompt Template: Code Review

Use when the Reviewer agent evaluates a module or pull request.

---

**Module / files:** [Path(s) to review]

**Review checklist:**
- [ ] PEP8 compliance
- [ ] Type hints on all public functions and methods
- [ ] Docstrings on all public classes and functions
- [ ] No hardcoded credentials, ports, or file paths
- [ ] Input validation at API boundaries
- [ ] Correct HTTP status codes
- [ ] Tests exist and cover edge cases and error paths
- [ ] No silently suppressed exceptions
- [ ] `.env` / secrets not committed

**Output format:** numbered list — each item: `[blocker|suggestion] file:line — description`.
