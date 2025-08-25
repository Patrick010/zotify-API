# Project Documentation Initiation Guide

## 1. Purpose
This document outlines the standard process for initiating the documentation for a new project using this template repository. Following this process ensures that all new projects start with a consistent, robust, and traceable documentation structure.

## 2. The Golden Rule: Use the Templates
The `templates/` directory is the single source of truth for all standard project documents. **Do not create documentation from scratch.** Always start by copying from the `templates/` directory.

## 3. Initiation Process

### Step 1: Copy Templates to the `project/` Directory
Your first step is to populate the `project/` directory with a full set of documentation. This documentation structure adheres to PRINCE2 best practices and guidelines to ensure robust project management.

1.  Review the full list of available templates in `templates/`.
2.  Copy all relevant templates into the `project/` directory, maintaining the subdirectory structure (e.g., `templates/logs/` -> `project/logs/`).
    *   **Note:** Not all templates may be applicable to every project. For example, if your project does not have a complex audit requirement, you may not need the files from `templates/audit/`. Use your judgment.

### Step 2: Create Any Additional Required Documents
If your project requires a standard document that is not yet in the `project/` directory (e.g., a `SECURITY.md` file), you must create it.

1.  **Consult the Template Registry:** First, review the `templates/PROJECT_REGISTRY.md` file to find a suitable template for the document you need. The registry lists all available templates and their intended roles.
2.  **Create from Template:** Copy the appropriate template from the `templates/` directory to your `project/` directory. **Never create a standard document from scratch.**
3.  **If No Template Exists:** In the rare case that a required document does not have a corresponding template, **do not proceed.** You must ask for guidance on which template to use as a base, or how to create a new one that aligns with the project's standards.

### Step 3: Populate the Placeholders
Once the files are copied, you must populate the placeholder values.

1.  Perform a project-wide search for the placeholder `<PROJECT_NAME>`.
2.  Replace all instances of `<PROJECT_NAME>` with the official name of your new project.
3.  Review each document for other placeholders (e.g., `<DATE>`, `<TEAM_MEMBER>`, `<STAKEHOLDER_ROLE>`) and fill them in with the correct information for your project.

### Step 4: Update the Project Registry
The `project/PROJECT_REGISTRY.md` is the master index for your documentation.

1.  Review the `project/PROJECT_REGISTRY.md` file.
2.  Ensure that all the documents you have created in the `project/` directory are correctly listed.
3.  If you have chosen not to include certain documents (e.g., the audit files), you may remove their entries from the registry to reflect the actual state of your project's documentation.

## 5. Next Steps
Once your documentation is initiated, the `project/ONBOARDING.md` file becomes the primary entry point for any new developer joining the project. It will guide them through the structure you have just created.
---
