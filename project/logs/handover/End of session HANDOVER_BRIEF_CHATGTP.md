You are tasked with **updating the session handover brief `HANDOVER_BRIEF_CHATGTP_<SESSION_TITLE>`** to reflect all knowledge and progress from the current session.  

Important: This handover must be written so the assistant can **internalize** the repo, workflows, and project state for direct continuation in the next session. Treat all scripts as artifacts to be studied and mapped, not executed. The final Markdown is primarily for assistant onboarding, but must also be clear enough for a new developer to use.  

The update must combine:

1. The previous handover content.  
2. **Session notes**: new decisions, scripts created or modified, workflows executed, tasks completed, dependencies, and unresolved items.

Your goal is to generate a **complete, self-contained Markdown handover** that any new session (or developer) can use to immediately understand the project state and continue work.

## Instructions

1. **Read the previous HANDOVER_BRIEF_CHATGTP_<SESSION_TITLE>.md **:

2. **Analyze session notes**:
   - Identify all new or modified scripts, workflows, documentation, or tests.
   - Record completed tasks, decisions, dependencies, and validation outcomes.
   - Note any unresolved items or follow-ups.

3. **Update the handover**:
   - Merge session notes into the existing handover extracted from the manifest.
   - Maintain clarity and structure in Markdown.
   - Ensure all references to files, scripts, indexes, and workflows are consistent with the manifest.
   - Include a **Session Summary** detailing what was done and achieved in this session.
   - Update **Tasks & Incremental Steps** and **Dependencies & References** accordingly.

4. **Maintain handover sections** (explicitly framed for assistant internalization):
   - **Introduction:** Current project status, context, and references to roadmap, PID, HLD/LLD, logs in `project/logs/`.
   - **Scripts & Workflows (to internalize, not execute):** Map each script or document to its role in workflows (audit, QA, docs, validation).
   - **Tasks & Incremental Steps (study objectives):** Include objectives, validation points, and progress. These are to be understood and tracked, not executed.  
   - **Decisions & Clarifications:** Explicit choices and rationale.  
   - **Dependencies & References:** Updated according to manifest.  
   - **Unresolved Items / Questions:** Pending follow-ups.  
   - **Session Summary:** Concise recap of what changed or progressed.  

5. **Output**:
   - Produce the updated `HANDOVER_BRIEF_CHATGTP.md` **entirely in Markdown**.
   - Highlight any newly added scripts, workflows, or changes from the current session.
   - Include a “Session Continuation Directives” section at the end — explicit, bullet-pointed handoff instructions for the next assistant (like “Next assistant should resume at Step X, validate Y, continue with Z”)

## Inputs

- **HANDOVER_BRIEF_CHATGTP.md:** Previous handover content.
- **Session Notes:** Text describing new scripts, workflows, decisions, and task progress.

## Constraints

- Do **not** execute any scripts or modify repo files.
- The handover must fully reflect **current project state** and serve as the onboarding document for the assistant to continue seamlessly.  
- Ensure clarity so a completely new session or developer can pick up seamlessly.

## Output Example

```markdown
# HANDOVER_BRIEF_CHATGTP.md

## Introduction
...

## Scripts & Workflows (to internalize, not execute)
...

## Tasks & Incremental Steps (study objectives)
...

## Decisions & Clarifications
...

## Dependencies & References
...

## Unresolved Items / Questions
...

## Session Summary
...