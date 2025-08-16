# Snitch Installation & Usage Guide

**Status:** Active
**Date:** 2025-08-16

## 1. Prerequisites

### 1.1. Go
Snitch is written in Go and requires a recent version of the Go toolchain to build and run.

**To install Go on Linux (Debian/Ubuntu):**
```bash
# Download the latest Go binary (check go.dev/dl/ for the latest version)
curl -OL https://go.dev/dl/go1.21.0.linux-amd64.tar.gz

# Install Go to /usr/local
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# Add Go to your PATH
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
source ~/.profile

# Verify the installation
go version
```

**To install Go on macOS or Windows:**
Please follow the official instructions on the [Go download page](https://go.dev/dl/).

### 1.2. Git
Git is required to clone the repository.
```bash
# On Debian/Ubuntu
sudo apt-get update && sudo apt-get install -y git
```

---

## 2. Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Patrick010/zotify-API
    ```

2.  **Navigate to the `snitch` directory:**
    ```bash
    cd zotify-API/snitch
    ```

3.  **Prepare Go modules:**
    Snitch is a self-contained module. To ensure your environment is set up correctly, run:
    ```bash
    go mod tidy
    ```
    This command will verify the `go.mod` file.

---

## 3. Running Snitch

Snitch must be configured with the callback URL of the main Zotify API before running.

1.  **Set the environment variable:**
    ```bash
    export SNITCH_API_CALLBACK_URL="http://localhost:8000/api/auth/spotify/callback"
    ```

2.  **Run the application:**
    From the `snitch` directory, execute the following command:
    ```bash
    go run ./cmd/snitch
    ```

3.  **Expected output:**
    You should see the following output, indicating Snitch is running:
    ```
    SNITCH: Listening on http://127.0.0.1:4381
    ```

---

## 4. Building Snitch

You can compile Snitch into a single executable for different operating systems.

### 4.1. Building for your current OS
From the `snitch` directory, run:
```bash
go build -o snitch ./cmd/snitch
```
This will create an executable named `snitch` in the current directory.

### 4.2. Cross-Compiling for Windows
From a Linux or macOS machine, you can build a Windows executable (`.exe`).

1.  **Set the target OS environment variable:**
    ```bash
    export GOOS=windows
    export GOARCH=amd64
    ```

2.  **Run the build command:**
    ```bash
    go build -o snitch.exe ./cmd/snitch
    ```
This will create an executable named `snitch.exe` in the current directory.

---

## 5. Troubleshooting
-   **Port in use**: If you see an error like `bind: address already in use`, it means another application is using port `4381`. Ensure no other instances of Snitch are running.
-   **`go` command not found**: Make sure the Go binary directory is in your system's `PATH`.
-   **`SNITCH_API_CALLBACK_URL` not set**: The application will panic on startup if this required environment variable is missing.
