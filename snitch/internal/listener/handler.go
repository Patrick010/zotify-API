package listener

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

// ipcPayload defines the structure of the JSON payload sent to the Zotify API.
type ipcPayload struct {
	Code string `json:"code"`
}

// newHandler creates a handler that validates a GET request from the browser,
// then sends the captured code to the main Zotify API via a POST request.
func newHandler(shutdown chan<- bool, expectedState, ipcToken string, ipcPort int) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 1. Validate GET request from browser
		code := r.URL.Query().Get("code")
		state := r.URL.Query().Get("state")

		if state != expectedState {
			log.Printf("Invalid state token received. Expected: %s, Got: %s", expectedState, state)
			http.Error(w, "Error: Invalid state token.", http.StatusBadRequest)
			// DO NOT shut down. Wait for a valid request or timeout.
			return
		}

		if code == "" {
			log.Println("Callback received without a code.")
			http.Error(w, "Error: Missing authorization code in callback.", http.StatusBadRequest)
			// Still shut down, because the state was valid and consumed.
			shutdown <- true
			return
		}

		// 2. Send captured code to Zotify API IPC server
		if err := sendCodeToAPI(code, ipcToken, ipcPort); err != nil {
			log.Printf("Failed to send code to Zotify API: %v", err)
			http.Error(w, "Error: Could not communicate with Zotify API. Please check logs.", http.StatusInternalServerError)
		} else {
			log.Println("Successfully sent code to Zotify API.")
			fmt.Fprintln(w, "Authentication successful! You can close this window now.")
		}

		// 3. Trigger shutdown regardless of IPC success/failure,
		// because the one-time-use code has been received.
		shutdown <- true
	}
}

// sendCodeToAPI makes a POST request to the main Zotify API to deliver the code.
func sendCodeToAPI(code, ipcToken string, ipcPort int) error {
	payload := ipcPayload{Code: code}
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal IPC payload: %w", err)
	}

	url := fmt.Sprintf("http://127.0.0.1:%d/zotify/receive-code", ipcPort)
	req, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(payloadBytes))
	if err != nil {
		return fmt.Errorf("failed to create IPC request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+ipcToken)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("failed to send IPC request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("IPC request failed with status code %d", resp.StatusCode)
	}

	return nil
}
