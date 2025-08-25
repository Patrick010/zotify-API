# Bootstrap Prompt: Project Onboarding

**Objective:** To bring any new developer fully up to speed on the Zotify API project.

**Instructions:**
Your primary goal is to gain a complete understanding of the project's current state, architecture, and processes. To do this, you must follow the "Recommended Onboarding Flow" outlined below, reviewing each document in the specified order. This sequential review is mandatory for efficient context restoration.

Upon completion, you will be fully aligned with the project's live status. At that point, please confirm you have completed the onboarding and await further instructions. Do not begin any development work until you receive a specific task.

---

## Your First Task: Review the Live Project State & Audit

**Your first and most important task is to understand the current, live state of the project's ongoing audit and development work.** Do not proceed to any other documents or tasks until you have completed this review.

This review is mandatory to ensure you are aligned with the project's immediate context and priorities.

**Required Reading Order:**

1.  **`project/logs/CURRENT_STATE.md`**: Start here. This document provides a narrative summary of the most recent activities, known issues, and the immediate next steps.
2.  **`project/logs/ACTIVITY.md`**: Read this second. It provides a reverse-chronological log of all significant tasks performed. This will give you a detailed history of how the project arrived at its current state.
3.	**`project/logs/SESSION_LOG.md`: Session reporting progress and findings document.
4.  **`project/audit/` Directory**: Finally, review the documents in this directory. They contain the detailed findings, plans, and traceability matrices for the ongoing architectural audit.

Once you have reviewed these documents, you will have a complete picture of the project's status.

---

# Zotify API Onboarding

**Status:** Live Document

## 1. Purpose

This document is intended to bring a new developer up to speed on the project, providing guidance for understanding the architecture, workflows, and key artifacts.

It is mandatory that developers **review these materials in order** to efficiently onboard without affecting live project workflows.

## 2. Key Onboarding Documents

To get a full understanding of the project, review the following documents:

1. **Current State**: Review `CURRENT_STATE.md` to understand the latest context and project state.
2. **Project Registry**: The master index for all project documents.
3. **Design Alignment Plan**: Provides current primary project goals and process guidance.
4. **Traceability Matrix**: Identifies gaps between design and implementation.
5. **Activity Log**: Chronological record of recent tasks.
6. **Session Log**: Log of activities and findings from sessions.
7. **Lessons Learnt**: Summary of process maturity and key takeaways.
8. **Project Initiation Document (PID)**: The formal 'living document' that defines the project's scope, plans, and controls.
9. **Backlog**: List of defined, pending tactical tasks.
10. **High-Level Design (HLD)** and **Low-Level Design (LLD)**: Refactored architecture documentation.
11. **Use Cases**: Defines target user scenarios.
12. **Use Cases Gap Analysis**: Shows current feature coverage and highlights development opportunities.

---

### 3. Recommended Onboarding Flow

1. Start with the **Key Onboarding Documents** to understand where the project stands.
2. Review **Design and Traceability artifacts** to see what is complete and what requires attention.
3. Consult the **Backlog** for actionable tasks.
4. Explore **Use Cases and Gap Analysis** to understand feature priorities.
5. Review **Lessons Learnt** to internalize process insights.
6. **Internalize the Definition of 'Done':** Review the `TASK_CHECKLIST.md`. This file defines the mandatory quality gate for all work. Before considering any task complete, ensure you have fulfilled all applicable checks it contains.

---

### 4. Notes

* All documents referenced are live and should be used as the primary source of truth.
* Filename changes are possible; always reference documents by their **role** in the Project Registry rather than the filename itself.
* Before a task or phase can be considered 'Done' or 'Completed', the Task Execution Checklist must be followed.
