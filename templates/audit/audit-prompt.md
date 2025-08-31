# Bootstrap Prompt: Comprehensive Reality Audit

## Goal

The primary goal of this task is to conduct a Comprehensive Reality Audit of the entire project. The final deliverable will be a single, authoritative markdown document that establishes a definitive baseline of the project's current state. This document will serve as the single source of truth for all future planning and development.

## Context

This type of audit is initiated when the project's documentation is suspected to be significantly out of sync with the implemented reality. The process is designed to uncover all discrepancies, contradictions, and fictional documentation, no matter how small. The audit is not a quick review; it is a meticulous, exhaustive, and brutally honest analysis.

## Required Process & Level of Detail

The audit report must be generated with an extreme level of detail. Summaries, wildcards, or aggregations are strictly forbidden.

The final audit document must contain the following sections:

    **Part 1.1: Complete API Endpoint Inventory**
        An exhaustive, line-by-line table of every unique API endpoint path found in the codebase.
        For each endpoint, list its HTTP method(s), functional status (e.g., Functional, Stub, Broken), and a brief, accurate description of its purpose.

    **Part 1.2: Complete Code File Inventory**
        An exhaustive, line-by-line table of all relevant source code files (e.g., .py, .go, .cs). The exact list of file types should be confirmed before starting.
        For each file, provide its full path and a concise, accurate description of its purpose.

    **Part 2: Complete Documentation Gap Analysis**
        This is the most critical part of the audit. You must first identify every single markdown (.md) file in the repository.
        You must then examine every single file on that list and create an exhaustive table containing:
            The full file path.
            A status (e.g., ✅ Accurate, ⚠️ Partially Inaccurate, ❌ Fictional/Outdated).
            A detailed "Gap Analysis" describing how the document's content deviates from the reality of the codebase.

    **Part 3: Final Recommendations**
        Based on the findings from the inventories and gap analysis, provide a set of concrete, actionable recommendations for the next phase of work.

## Gold Standard Example & Point of Reference

The canonical example of a completed audit that meets the required level of detail can be found in this repository at: `<link_to_example_audit_document>`

You must use this file as the gold standard for the structure and detail of your final report. Note that the process of creating a reference audit may involve several painful but necessary correction loops. Your goal is to learn from that history and produce a correct and complete report on the first attempt by adhering strictly to the level of detail described above.
