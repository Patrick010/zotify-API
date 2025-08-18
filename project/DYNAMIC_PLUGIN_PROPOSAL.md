# Proposal: Dynamic Plugin System for Logging Sinks

**Date:** 2025-08-18
**Author:** Jules
**Status:** Proposed

## 1. Problem Statement

The current Flexible Logging Framework is highly configurable but not easily extensible. While administrators can define new *instances* of existing sink types (`console`, `file`, `webhook`) in the `logging_framework.yml` file, adding a new *type* of sink (e.g., a `SyslogSink`, `KafkaSink`, or a custom database logger) requires direct modification of the core Zotify API codebase, specifically the `service.py` file.

This violates the principle of a truly flexible and extensible system and creates a bottleneck for developers who may wish to integrate the API's logging with their own infrastructure without needing to fork and modify the core project.

## 2. Proposed Solution

This document proposes the implementation of a **dynamic plugin system** for the Flexible Logging Framework, based on Python's standard `entry_points` packaging metadata.

This system will allow third-party developers to create their own custom sink implementations in separate, installable Python packages. The Zotify API will then be able to automatically discover and use these custom sinks if they are installed in the same Python environment.

### 2.1. How It Will Work

1.  **Defining the Plugin Interface:** The Zotify API will define a specific entry point, for example, `zotify.logging.sinks`. This serves as a public contract for any potential plugin.

2.  **Creating a Plugin:** A developer wanting to create a new `SyslogSink` would create a new, separate Python package (e.g., `zotify-syslog-sink`). In their package's `pyproject.toml`, they would register their custom sink class against the Zotify API's entry point:
    ```toml
    [project.entry-points."zotify.logging.sinks"]
    syslog = "zotify_syslog_sink.main:SyslogSink"
    ```

3.  **Plugin Discovery:** The Zotify API's `LoggingService` will be modified. On startup, it will use Python's `importlib.metadata` to scan the environment for all installed packages that have registered a plugin for the `zotify.logging.sinks` entry point.

4.  **Plugin Instantiation:** The `LoggingService` will add these discovered plugins to its list of available sink types. When it encounters a sink with `type: syslog` in the `logging_framework.yml`, it will know how to load the `SyslogSink` class from the plugin package and instantiate it.

## 3. Benefits

-   **True Extensibility:** Developers can add entirely new logging capabilities without ever touching the core API code, promoting a healthy ecosystem of community-driven extensions.
-   **Decoupling:** The core API does not need to know about any specific plugin implementation. It only needs to know how to discover and load plugins that adhere to the contract.
-   **Future-Proofing:** This makes the framework adaptable to any future logging or notification technology.

## 4. High-Level Implementation Plan

1.  **Modify `LoggingService` (`service.py`):**
    -   In the `__init__` or `load_config` method, add a discovery mechanism using `importlib.metadata.entry_points()`.
    -   Iterate through the discovered plugins for the `zotify.logging.sinks` group.
    -   Store the discovered plugin classes in a dictionary, mapping the sink `type` (e.g., `"syslog"`) to the loaded class.
    -   When instantiating sinks from the YAML, if the `type` is not one of the built-in types, look it up in the dictionary of discovered plugins.

2.  **Define a Clear Plugin Interface:**
    -   Ensure that the `BaseSink` class in `service.py` is well-documented and serves as the stable abstract base class that all custom sink plugins must inherit from.

3.  **Update Documentation:**
    -   Create a new `PLUGIN_DEVELOPMENT_GUIDE.md` that explains in detail how to create a custom sink package, how to register the entry point, and how to test it.
    -   Update the `LOGGING_GUIDE.md` to mention that the framework is extensible and link to the new plugin development guide.

4.  **Create a Reference Implementation:**
    -   To validate the system, create a simple, separate example plugin package (e.g., `zotify-print-sink`) that provides a basic `PrintSink` and document how to install and use it.
