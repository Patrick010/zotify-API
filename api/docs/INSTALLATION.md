# Installation

This document provides detailed instructions for installing and setting up the Zotify REST API.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.10 or greater**
- **FFmpeg**: A cross-platform solution to record, convert and stream audio and video.
- **Docker**: (Optional) For the Docker-based installation.

## Installation Methods

You can choose one of the following methods to install the Zotify API.

### 1. Git Clone (Recommended for Developers)

This method requires **Git** to be installed. It involves cloning the repository and installing the dependencies manually.

1.  **Clone the Zotify repository:**
    ```bash
    git clone https://github.com/Googolplexed0/zotify.git
    cd zotify
    ```

2.  **Navigate to the API directory:**
    ```bash
    cd api
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: We will create this requirements.txt file from pyproject.toml in a later step)*

4.  **Run the API server:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8080
    ```

### 2. Installation Script

An installation script will be provided to automate the setup process.

*(This section is a placeholder and will be updated with the script details.)*

### 3. Debian Package (`.deb`)

A Debian package will be created for easy installation on Debian-based systems like Ubuntu.

*(This section is a placeholder and will be updated with package details.)*

### 4. Docker

Using Docker is a great way to run the API in a containerized environment.

1.  **Build the Docker image:**
    *(A Dockerfile will be created in a later step)*
    ```bash
    docker build -t zotify-api .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8080:8080 zotify-api
    ```

This will start the API server inside a Docker container, accessible on port 8080 of your host machine.
