<!-- ID: API-203 -->
# Project Code Quality Index

This document tracks the quality of every source code file in the project. Each file is assessed against the rubric defined below.

## Scoring Rubric

Each file is assigned two independent quality scores: one for **Documentation (`Doc Score`)** and one for **Code (`Code Score`)**.

### Documentation Score
This score assesses the quality, completeness, and clarity of comments and docstrings.

| Grade | Criteria |
| :---: | --- |
| **A** | **Excellent:** Comprehensive module, class, and function docstrings are all present and follow a consistent style. All public methods are documented. Complex logic, algorithms, and business rules are explained with inline comments. |
| **B** | **Good:** Most public methods have docstrings, but they may lack detail or consistency. Some complex logic is commented, but not all. |
| **C** | **Needs Improvement:** Docstrings are sparse or missing for many methods. Little to no inline comments to explain complex sections. A new developer would struggle to understand the file's purpose without reading the code. |
| **D** | **Poor:** Only a few, minimal docstrings or comments exist. The file is effectively undocumented. |
| **F** | **Unacceptable:** No docstrings or comments whatsoever. |

### Code Quality Score
This score assesses the implementation's clarity, efficiency, structure, and testability.

| Grade | Criteria |
| :---: | --- |
| **A** | **Excellent:** Code is clear, efficient, and well-structured, following established design patterns. It has high, meaningful unit test coverage (>90%). Logic is simple and easy to follow. |
| **B** | **Good:** Code is functional but could be improved. It might be slightly inefficient, have some overly complex functions, or have only moderate test coverage (50-90%). |
| **C** | **Needs Improvement:** Code is difficult to understand, contains significant technical debt (e.g., large functions, deep nesting, magic numbers), or has low test coverage (<50%). |
| **D** | **Poor:** Code is highly inefficient, convoluted, or buggy. It may have little to no test coverage and poses a maintenance risk. |
| **F** | **Unacceptable:** Code is non-functional, contains critical bugs, or is a direct copy-paste from another source without adaptation. |

---

## API Module

| File Path | Documentation Score | Code Score | Overall Score | Notes |
| --- | :---: | :---: | :---: | --- |
| `api/src/zotify_api/auth_state.py` | B | A | A | Good comments explaining the module's purpose and the in-memory nature of the PKCE state. Code is clean and uses type hints. |
| `api/src/zotify_api/config.py` | C | B | B | Uses Pydantic for settings, which is good. However, the file lacks module and class docstrings. The module-level logic for handling production key checks and development defaults has side-effects and could be encapsulated in a factory function for better structure. |
| `api/src/zotify_api/globals.py` | D | C | D | File defines a global variable based on module import time, which is a problematic pattern for testing and predictability. It also lacks any documentation explaining its purpose. |
| `api/src/zotify_api/logging_config.py` | D | F | F | A simple file that appears to be a remnant of an old logging system. It lacks all documentation and its approach contradicts the project's new Flexible Logging Framework. Code is non-functional in the context of the current design. |
| `api/src/zotify_api/main.py` | B | B | B | Well-structured main application file. Most functions are well-documented, but it lacks a module-level docstring. The initialization logic is good, but could be improved by avoiding hardcoded filenames and making the error handler's configuration loading consistent with the logging framework's. |
| `api/src/zotify_api/core/error_handler/__init__.py` | A | A | A | Excellent implementation of a singleton error handler with clear documentation and a well-defined public API. |
| `api/src/zotify_api/core/error_handler/config.py` | A | A | A | A textbook example of how to use Pydantic for clear, self-documenting configuration models. |
| `api/src/zotify_api/core/error_handler/formatter.py` | B | A | A | Clean implementation of the strategy pattern for error formatting. Docstrings could be slightly more detailed. |
| `api/src/zotify_api/core/error_handler/hooks.py` | B | B | B | Robust implementation of system-wide exception hooks. Code is solid but could be improved by mapping exception types to status codes instead of hardcoding 500. Documentation is good but could be more complete for internal functions. |
| `api/src/zotify_api/core/error_handler/triggers.py` | A | A | A | Excellent, extensible design for a trigger/action system using dynamic module loading. The code is robust and well-documented. |
| `api/src/zotify_api/core/error_handler/actions/__init__.py` | B | A | A | Standard package marker with a helpful comment. |
| `api/src/zotify_api/core/error_handler/actions/log_critical.py` | A | A | A | Excellent, well-documented example of a trigger action that integrates cleanly with the logging framework. |
| `api/src/zotify_api/core/error_handler/actions/webhook.py` | B | F | F | The core logic of this action is commented out, making it a non-functional stub. |
| `api/src/zotify_api/core/logging_framework/__init__.py` | A | A | A | A perfect example of a clean public API that decouples the interface from the implementation. |
| `api/src/zotify_api/core/logging_framework/filters.py` | A | B | A | A clear and effective implementation of a sensitive data filter. The regex-based approach is good, though a more robust solution could handle complex edge cases. |
| `api/src/zotify_api/core/logging_framework/schemas.py` | B | A | A | An excellent and robust configuration schema using advanced Pydantic features. A few more high-level docstrings would make it perfect. |
| `api/src/zotify_api/core/logging_framework/service.py` | C | B | B | A sophisticated logging service with an advanced feature set. However, it is significantly under-documented, and some sink implementations (like console and webhook) are incomplete or not robust. |
| `api/src/zotify_api/core/logging_handlers/__init__.py` | B | A | A | Standard package marker with a helpful comment. |
| `api/src/zotify_api/core/logging_handlers/base.py` | A | A | A | Perfect implementation of an abstract base class for a strategy pattern. |
| `api/src/zotify_api/core/logging_handlers/console_handler.py` | B | B | B | Clean and simple implementation of a console log handler. |
| `api/src/zotify_api/core/logging_handlers/database_job_handler.py`| B | B | B | Robust and safe implementation of a database log handler. Code is clear and handles transactions correctly. |
| `api/src/zotify_api/core/logging_handlers/json_audit_handler.py` | B | A | A | Excellent implementation of a structured JSON audit logger with robust formatting and error handling. |
| `api/src/zotify_api/database/__init__.py` | F | A | C | File is completely empty. A comment explaining its purpose as a package marker would be beneficial. |
| `api/src/zotify_api/database/crud.py` | A | B | A | A very well-documented and clear set of CRUD functions. The code is clean and correct, with only minor opportunities for performance optimization. |
| `api/src/zotify_api/database/models.py` | C | A | B | An excellent, modern implementation of the database schema using SQLAlchemy 2.0. However, the file is significantly under-documented, lacking docstrings for the module, classes, and key columns. |
| `api/src/zotify_api/database/session.py` | B | A | A | A textbook implementation of a SQLAlchemy session for FastAPI. Clean, correct, and well-documented where it matters most. |
| `api/src/zotify_api/middleware/request_id.py` | D | D | D | The middleware is functionally incorrect as it generates the request ID after the request has been processed, making it unavailable to any downstream logic. The file also lacks any documentation. |
| `api/src/zotify_api/models/config_models.py` | C | A | B | Excellent use of Pydantic for request models, but lacks docstrings to explain the purpose of the models. |
| `api/src/zotify_api/models/sync.py` | C | A | B | A simple and correct Pydantic model that lacks documentation. |
| `api/src/zotify_api/providers/__init__.py` | F | A | C | File is completely empty. A comment explaining its purpose as a package marker would be beneficial. |
| `api/src/zotify_api/providers/base.py` | A | A | A | A perfect example of an abstract base class that clearly defines the provider interface. |
| `api/src/zotify_api/providers/spotify_connector.py` | B | D | D | The connector is well-documented but has significant architectural issues (improper global state, hardcoded HTML, fragile dependencies) that make it difficult to maintain. |
| `api/src/zotify_api/routes/__init__.py` | B | A | A | Standard package marker with a helpful comment. |
| `api/src/zotify_api/routes/auth.py` | A | B | A | Clean, well-documented auth routes. The `logout` endpoint contains a known design issue that needs to be addressed. |
| `api/src/zotify_api/routes/cache.py` | A | A | A | A textbook example of a clean, well-documented route file that properly separates concerns. |
| `api/src/zotify_api/routes/config.py` | F | A | C | An excellent, clean implementation of config routes, but it is completely undocumented. |
| `api/src/zotify_api/routes/downloads.py` | B | C | C | Clean, well-documented routes. The service layer is tightly coupled via a direct import instead of using FastAPI's dependency injection system, making it difficult to test. |
| `api/src/zotify_api/routes/network.py` | F | A | C | Excellent, clean implementation of network routes, but it is completely undocumented. |
| `api/src/zotify_api/routes/notifications.py`| D | C | D | Clean implementation of notification routes, but it is undocumented and uses a generic dictionary for a response model instead of a specific Pydantic schema. |
| `api/src/zotify_api/routes/playlists.py`| F | A | C | A textbook example of a robust and well-structured route file with excellent error handling and specific schemas, but it is completely undocumented. |
| `api/src/zotify_api/routes/search.py` | F | C | D | The route is undocumented and uses direct service imports instead of dependency injection, making it hard to test. The feature flag implementation is also unconventional. |
| `api/src/zotify_api/routes/sync.py` | B | C | C | The route has a docstring, but the implementation is overly complex and tightly coupled due to direct service imports and a broad exception handler. |
| `api/src/zotify_api/routes/system.py` | B | B | B | The implemented system routes are clean and well-documented. The unimplemented routes correctly return a 501 status. |
| `api/src/zotify_api/routes/tracks.py` | C | C | C | A mix of good and bad practices. Some routes are clean, while others use direct imports and poor exception handling. Documentation is also inconsistent. |
| `api/src/zotify_api/routes/user.py` | F | B | C | Clean implementation of user-related routes that correctly uses dependency injection, but is completely undocumented and uses generic dictionaries for some response models. |
| `api/src/zotify_api/routes/webhooks.py` | F | B | C | Clean implementation that correctly uses background tasks, but is completely undocumented and uses direct service imports. |
| `api/src/zotify_api/schemas/auth.py` | C | A | B | Clear and correct Pydantic models for authentication flows, but they lack documentation. |
| `api/src/zotify_api/services/__init__.py` | F | A | C | Empty file. |
| `api/src/zotify_api/services/auth.py` | B | C | C | Service has good documentation for its main functions but is tightly coupled to global state (`pending_states`), making it difficult to test and maintain. Error handling could be more specific. |
| `api/src/zotify_api/services/cache_service.py` | A | B | A | Excellent documentation. Code is clean but uses a mock in-memory cache instead of a real one, which is a significant simplification. |
| `api/src/zotify_api/services/config_service.py`| A | A | A | Excellent code that correctly handles loading, updating, and resetting a JSON-backed config file. |
| `api/src/zotify_api/services/db.py` | F | C | D | Undocumented. The code is a simple factory function, but it's not robust (e.g., doesn't handle connection errors). |
| `api/src/zotify_api/services/deps.py` | B | B | B | The docstrings are good. The `get_spoti_client` dependency is well-written and handles token refreshing correctly. The `get_provider_no_auth` has a hardcoded string `"spotify"`, which is not ideal. |
| `api/src/zotify_api/services/download_service.py`| C | B | B | Undocumented functions. The logic is clean and correctly uses the CRUD layer. The `process_download_queue` function simulates I/O with `time.sleep`, which is fine for a service like this. |
| `api/src/zotify_api/services/logging_service.py`| B | D | D | Good class docstring. The code is overly complex and seems to be a remnant of a different design than the one in `core/logging_framework`. |
| `api/src/zotify_api/services/metadata_service.py`| F | D | F | Undocumented. Uses a global in-memory dictionary for storage, which is not a scalable or persistent solution. |
| `api/src/zotify_api/services/network_service.py`| B | B | B | Good documentation. The code is a simple in-memory service, similar to `cache_service`. |
| `api/src/zotify_api/services/notifications_service.py`| F | B | C | Undocumented. The service correctly depends on `user_service` to manage its data, which is a good example of separation of concerns. |
| `api/src/zotify_api/services/playlists_service.py`| F | B | C | Undocumented. The code is well-structured, defines a custom exception, and uses the database engine correctly. The limit/offset normalization is robust. |
| `api/src/zotify_api/services/search.py` | F | D | F | Undocumented. The use of raw SQL with string formatting is a significant security and maintenance issue. |
| `api/src/zotify_api/services/spoti_client.py`| B | A | A | Good class docstring, but many methods are undocumented. The code itself is an excellent, robust `httpx`-based client for the Spotify API. |
| `api/src/zotify_api/services/sync_service.py` | B | C | C | Good function docstring. The service is just a stub that prints a message. |
| `api/src/zotify_api/services/tracks_service.py`| C | D | D | Some functions are documented. The code uses raw SQL, which is inconsistent with the ORM (`crud.py`) used elsewhere. The `get_tracks_metadata_from_spotify` function contains a "hack" to get around a gap in the provider abstraction. |
| `api/src/zotify_api/services/user_service.py` | B | B | B | Good documentation. The service correctly encapsulates all user-related data and logic, reading from and writing to a JSON file for persistence. |
| `api/src/zotify_api/services/webhooks.py` | F | B | C | Undocumented. The code correctly uses a background task for firing webhooks to avoid blocking the request. |

## Snitch Module

| File Path | Documentation Score | Code Score | Overall Score | Notes |
|---|:---:|:---:|:---:|---|
| `snitch/snitch.go` | C | B | C | Excellent inline comments and a clear module-level comment. Lacks function-level docstrings, which is a significant gap. |

## Gonk-TestUI Module

| File Path | Documentation Score | Code Score | Overall Score | Notes |
|---|:---:|:---:|:---:|---|
| `Gonk/GonkUI/app.py` | C | B | C | The core Flask routes are clear, but the functions for managing the `sqlite-web` subprocess are complex and lack docstrings. |
| `Gonk/GonkUI/static/app.js` | C | B | C | Excellent inline comments, but lacks function-level docstrings for complex UI state management. |
| `Gonk/GonkUI/static/styles.css` | A | A | A | Excellent use of CSS variables and a clear, logical structure. |
| `Gonk/GonkUI/templates/index.html` | A | A | A | Clean, semantic HTML5 structure. |

## Scripts Module

| File Path | Documentation Score | Code Score | Overall Score | Notes |
|---|:---:|:---:|:---:|---|
| `scripts/validate_code_index.py` | F | F | F | New file, pending review. |
| `scripts/lint_governance_links.py` | B | B | B | Refactored to handle multiple `TRACE_INDEX.yml` formats, improving robustness and backward compatibility. The code is now more resilient to changes in the trace index schema. |
| `scripts/repo_inventory_and_governance.py` | X | X | X | File was modified to fix a bug in audit report generation and to ignore the `site/` directory. Pending new quality review. |
| `scripts/linter.py` | X | X | X | File has been significantly refactored to integrate manifest generation; pending new quality review. |
| `scripts/generate_alignment_audit_report.py` | X | X | X | Initial implementation |
