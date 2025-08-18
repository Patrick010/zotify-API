package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"regexp"
	"time"
)

// --- Globals & Constants ---

const listenAddr = "127.0.0.1:4381"
var paramValidator = regexp.MustCompile(`^[a-zA-Z0-9\-_.~]+$`)
var logger = log.New(os.Stdout, "SNITCH: ", log.Ldate|log.Ltime|log.Lshortfile)

// --- Main Application Logic ---

func main() {
	logger.Println("Starting snitch on", listenAddr)

	// Get required environment variable
	apiCallbackURL := os.Getenv("SNITCH_API_CALLBACK_URL")
	if apiCallbackURL == "" {
		logger.Fatal("FATAL: Required environment variable SNITCH_API_CALLBACK_URL is not set")
	}

	// The handler now gets the callback URL via a closure
	http.HandleFunc("/login", loginHandler(apiCallbackURL))

	server := &http.Server{
		Addr:         listenAddr,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  15 * time.Second,
	}

	if err := server.ListenAndServe(); err != nil {
		logger.Fatalf("Could not start server: %s\n", err)
	}
}

// --- HTTP Handler ---

func loginHandler(apiCallbackURL string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		logger.Printf("event: callback.received, details: {method: %s, path: %s}", r.Method, r.URL.Path)

		// --- Input Validation ---
		code := r.URL.Query().Get("code")
		state := r.URL.Query().Get("state")
		errorParam := r.URL.Query().Get("error")

		if errorParam != "" {
			writeGenericError(w, "callback.validation.failure", map[string]interface{}{"reason": "provider_error", "error": errorParam})
			return
		}

		if !paramValidator.MatchString(code) || code == "" {
			writeGenericError(w, "callback.validation.failure", map[string]interface{}{"reason": "invalid_code_param"})
			return
		}

		if !paramValidator.MatchString(state) || state == "" {
			writeGenericError(w, "callback.validation.failure", map[string]interface{}{"reason": "invalid_state_param"})
			return
		}

		logger.Printf("event: callback.validation.success, details: {state_len: %d}", len(state))

		// --- Secret Handling & Handoff ---
		logger.Printf("event: callback.handoff.started, details: {code_len: %d}", len(code))

		// Construct the URL with query parameters
		url := fmt.Sprintf("%s?code=%s&state=%s", apiCallbackURL, code, state)

		// Use the correct HTTP GET method
		resp, err := http.Get(url)
		if err != nil {
			writeGenericError(w, "callback.handoff.failure", map[string]interface{}{"reason": "get_request_error", "error": err.Error()})
			return
		}
		defer resp.Body.Close()

		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			writeGenericError(w, "callback.handoff.failure", map[string]interface{}{"reason": "read_response_error", "error": err.Error()})
			return
		}

		if resp.StatusCode >= 400 {
			logger.Printf("event: callback.handoff.failure, details: {status_code: %d, response: %s}", resp.StatusCode, string(respBody))
			w.WriteHeader(resp.StatusCode)
			fmt.Fprintln(w, "Authentication failed on the backend server.")
			return
		}

		logger.Printf("event: callback.handoff.success, details: {status_code: %d}", resp.StatusCode)
		w.WriteHeader(resp.StatusCode)
		w.Write(respBody)
	}
}

func writeGenericError(w http.ResponseWriter, eventName string, details map[string]interface{}) {
	logger.Printf("event: %s, details: %v", eventName, details)
	http.Error(w, "Authentication failed. Please close this window and try again.", http.StatusBadRequest)
}
