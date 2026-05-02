# Prompt Template: Implement Feature

Use when the Developer agent implements a plan step.

---

**Plan step:** [Step number and title from `plans/entregableN.md`]

**Inputs:**
- Instruction file: `instructions/entregableN.md`
- Approved architecture: [reference to decision in plan]
- Existing code: [relevant file paths]

**Requirements:**
- [Bullet list of specific requirements for this step]

**Acceptance criteria:**
- [Criteria from the plan step]

**Constraints:**
- Follow all rules in `CLAUDE.md`.
- Do not modify files outside the scope of this step.
- Write or update tests alongside the implementation.
