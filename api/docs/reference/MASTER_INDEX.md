# API Documentation Master Index

This document serves as the central index for all **technical documentation** related to the Zotify API and its sub-modules. All new technical documentation files must be registered here.

**Note:** This index is for API-specific technical documentation. For high-level project management and architectural documents, please see the [Project Registry](../../project/PROJECT_REGISTRY.md).

## Core API

*   [API Reference](API_REFERENCE.md)
*   [Code Quality Index](CODE_QUALITY_INDEX.md)
*   [Feature Specifications](FEATURE_SPECS.md)

## Manuals

*   [API Developer Guide](../manuals/API_DEVELOPER_GUIDE.md)
*   [CI/CD Guide](../manuals/CICD.md)
*   [Error Handling Guide](../manuals/ERROR_HANDLING_GUIDE.md)
*   [Logging Guide](../manuals/LOGGING_GUIDE.md)
*   [Operator Manual](../manuals/OPERATOR_MANUAL.md)
*   [System Integration Guide](../manuals/SYSTEM_INTEGRATION_GUIDE.md)
*   [User Manual](../manuals/USER_MANUAL.md)

## System Design

*   [Error Handling Design](../system/ERROR_HANDLING_DESIGN.md)
*   [Installation Guide](../system/INSTALLATION.md)
*   [Privacy Compliance](../system/PRIVACY_COMPLIANCE.md)
*   [System Requirements](../system/REQUIREMENTS.md)

## Features

*   [Authentication](features/AUTHENTICATION.md)
*   [Automated Documentation Workflow](features/AUTOMATED_DOCUMENTATION_WORKFLOW.md)
*   [Developer Flexible Logging Framework](features/DEVELOPER_FLEXIBLE_LOGGING_FRAMEWORK.md)
*   [Provider Agnostic Extensions](features/PROVIDER_AGNOSTIC_EXTENSIONS.md)
*   [Provider OAuth](features/PROVIDER_OAUTH.md)

## Source Code Documentation

*   [CRUD Module](source/CRUD.py.md)
*   [Tracks Service](source/TRACKS_SERVICE.py.md)

## Providers

*   [Spotify Provider](../providers/SPOTIFY.md)

---

## Documentation Build Setup

The documentation site is built from multiple directories. To build the site locally, you must create symbolic links from the `api/docs` directory to the other documentation locations.

From the repository root, run the following commands:

```bash
ln -s ../../snitch/docs/ api/docs/snitch
ln -s ../../gonk-testUI/docs/ api/docs/gonk-testUI
ln -s ../../project/ api/docs/project
```
