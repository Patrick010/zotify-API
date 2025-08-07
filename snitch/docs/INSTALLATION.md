# Prerequisites

This guide provides instructions for setting up and running the Snitch module on a Debian-based Linux distribution.

### OS
- **Linux (Debian-based)**: Instructions are tailored for this OS.
- **macOS**: Steps should be similar, but package management commands will differ.
- **Windows**: Not officially supported for development at this time.

### Go
- **Go (latest version)**: Snitch requires the latest version of Go.

To install Go on Debian, we recommend the official binary distribution.

1.  **Download the latest Go binary:**
    ```bash
    curl -OL https://go.dev/dl/go1.24.3.linux-amd64.tar.gz
    ```
    *(Check the [Go download page](https://go.dev/dl/) for the absolute latest version.)*

2.  **Install Go:**
    ```bash
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.24.3.linux-amd64.tar.gz
    ```

3.  **Add Go to your PATH:**
    ```bash
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
    source ~/.profile
    ```

4.  **Verify the installation:**
    ```bash
    go version
    ```

### Git
- **Git**: Required to clone the repository.
    ```bash
    sudo apt-get update && sudo apt-get install -y git
    ```

### Optional Tools
- **curl** or a web browser: For manually testing the OAuth callback.
    ```bash
    sudo apt-get install -y curl
    ```

# Clone and Navigate

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Patrick010/zotify-API
    ```

2.  **Navigate to the `snitch` directory:**
    ```bash
    cd Zotify-API/snitch
    ```

# Go Setup

1.  **Initialize Go modules:**
    Snitch is a self-contained module with no external dependencies. To ensure your environment is set up correctly, run:
    ```bash
    go mod tidy
    ```
    This command will verify the `go.mod` file and download any necessary standard library dependencies if they are missing.

2.  **Confirm dependencies:**
    After running `go mod tidy`, you should see no changes if your Go installation is correct.

# Run Snitch (Temporary HTTP Listener)

1.  **Run the Snitch listener:**
    From the `snitch` directory, execute the following command:
    ```bash
    go run cmd/snitch/main.go
    ```

2.  **Expected output:**
    You should see the following output in your terminal, indicating that Snitch is running and waiting for a connection:
    ```
    INFO:snitch:Snitch is listening on http://localhost:21371/callback
    INFO:snitch:Waiting for Spotify to redirect... The listener will time out in 2 minutes.
    ```
    The listener will automatically shut down after 2 minutes if it does not receive a callback.

# Manual Spotify OAuth Test

To test that Snitch is working correctly, you can simulate the redirect from Spotify's authentication server.

1.  **Construct the redirect URL:**
    The URL must contain a `code` and a `state` parameter. For testing purposes, these can be any value.
    Example:
    `http://localhost:21371/callback?code=ABC123&state=xyz`

2.  **Open the URL in a browser or use `curl`:**
    - **Browser**: Paste the URL into your browser's address bar and press Enter. The browser will display a success message.
    - **curl**: Open a new terminal window and run the following command:
      ```bash
      curl "http://localhost:21371/callback?code=ABC123&state=xyz"
      ```

3.  **Expected console output:**
    In the terminal where Snitch is running, you should see the `code` printed to standard output, followed by shutdown messages:
    ```
    ABC123
    INFO:snitch:Successfully received OAuth code.
    INFO:snitch:Shutdown signal received, stopping listener...
    INFO:snitch:Snitch has shut down.
    ```

# Troubleshooting

-   **Port in use**: If you see an error like `bind: address already in use`, it means another application is using port `21371`. Ensure no other instances of Snitch or other services are running on that port.
-   **Go install issues**: If the `go` command is not found, make sure `/usr/local/go/bin` is in your `PATH` and you have sourced your `.profile` file or logged out and back in.
-   **Module not found**: If you get an error related to a module not being found, ensure you are in the `Zotify-API/snitch` directory before running the `go run` command.
-   **How to rerun**: If the listener times out or you want to run it again, simply execute the `go run cmd/snitch/main.go` command again.

# Planned Improvements

This is an early version of Snitch. Future improvements include:
-   **Dynamic Port**: Later versions will randomize the port and check for availability to avoid conflicts.
-   **Configuration**: The port and other settings will eventually be configurable via a `.env` file or command-line flags.
