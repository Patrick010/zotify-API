package listener

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

// CallbackPayload is the structure of the JSON payload sent to the FastAPI backend.
type CallbackPayload struct {
	Code  string `json:"code"`
	State string `json:"state"`
}

// handleCallback is the HTTP handler for the /login endpoint.
func handleCallback(w http.ResponseWriter, r *http.Request) {
	// 1. Extract code and state from query parameters
	code := r.URL.Query().Get("code")
	state := r.URL.Query().Get("state")

	if code == "" || state == "" {
		log.Println("[ERROR] Callback received with missing code or state.")
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		http.Error(w, "<h1>Authentication Failed</h1><p>Required 'code' or 'state' parameter was missing. Please try again.</p>", http.StatusBadRequest)
		return
	}

	// 2. Log them visibly to the console
	log.Printf("[INFO] Callback received. Code: %s, State: %s\n", code, state)

	// 3. Forward them as JSON in a POST request to the FastAPI backend
	payload := CallbackPayload{
		Code:  code,
		State: state,
	}

	jsonBytes, err := json.Marshal(payload)
	if err != nil {
		log.Printf("[ERROR] Failed to marshal payload: %v\n", err)
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		http.Error(w, "<h1>Authentication Failed</h1><p>Internal error: could not prepare data.</p>", http.StatusInternalServerError)
		return
	}

	// The backend URL is fixed for now as per requirements.
	apiURL := "http://192.168.20.5/auth/spotify/callback"
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Post(apiURL, "application/json", bytes.NewBuffer(jsonBytes))
	if err != nil {
		log.Printf("[ERROR] Failed to POST to backend API: %v\n", err)
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		http.Error(w, "<h1>Authentication Failed</h1><p>Could not connect to the application backend.</p>", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	log.Printf("[INFO] Forwarded callback data to backend. Backend responded with status: %d\n", resp.StatusCode)

	// 4. Show a user-facing HTML page in the browser
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if resp.StatusCode == http.StatusOK {
		fmt.Fprintln(w, "<h1>Authentication Successful</h1><p>You can close this window now.</p>")
	} else {
		fmt.Fprintln(w, "<h1>Authentication Failed</h1><p>The application backend rejected the request. Please check the application logs for more details.</p>")
	}
}
