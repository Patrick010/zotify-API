# Installation Guide

This document provides detailed instructions for installing and setting up the Zotify API.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python 3.10 or greater**
-   **pip**: The Python package installer.
-   **Git**: For cloning the repository.

## Installation

This installation guide is for developers and operators who want to run the API from the source code.

### 1. Clone the Repository

First, clone the project repository from GitHub to your local machine:
```bash
git clone https://github.com/Patrick010/zotify-API.git
cd zotify-API
```

### 2. Install Dependencies

The API's dependencies are listed in `api/pyproject.toml`. It is highly recommended to use a Python virtual environment.

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies from within the project root
pip install -e ./api
```

### 3. Configure the Environment

The API requires several environment variables to be set. The recommended way to manage these is with a `.env` file located in the `api/` directory. The application will automatically load this file on startup.

**Example `.env` file for Production:**
```
APP_ENV="production"
ADMIN_API_KEY="your_super_secret_admin_key"
DATABASE_URI="sqlite:///storage/zotify.db"
```

### 4. Running the API

The application is run using `uvicorn`, a high-performance ASGI server.

To run the server, execute the following command from the `/api` directory:
```bash
uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000
```

For development, you can enable hot-reloading:
```bash
uvicorn zotify_api.main:app --reload
```

## Running the Test Suite

Follow these steps to run the test suite.

### 1. Create the Storage Directory

The API requires a `storage` directory for its database and other files during tests. From the root of the project, create it inside the `api` directory:
```bash
mkdir api/storage
```

### 2. Run Pytest

The test suite requires the `APP_ENV` environment variable to be set to `test`. You must set this variable when you run `pytest`.

From inside the `api` directory, run:
```bash
APP_ENV=test python3 -m pytest
```
This will discover and run all tests in the `tests/` directory.
