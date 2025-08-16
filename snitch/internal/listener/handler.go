package listener

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"regexp"
)

var (
	// A simple regex to validate that the code and state are reasonable.
	// This is not a security measure, but a basic sanity check.
	// In a real scenario, the state would be a JWT or a random string of a fixed length.
	paramValidator = regexp.MustCompile(`^[a-zA-Z0-9\-_.~]+$`)
)

// validateState is a placeholder for the logic that would validate the state parameter.
// In a real implementation, this would likely involve a call to the main Zotify API
// or a cryptographic validation of a JWT.
func validateState(state string) bool {
	// For this simulation, we will just check if the state is not empty.
	return state != ""
}

func writeGenericError(w http.ResponseWriter, logger *log.Logger, eventName string, details map[string]interface{}) {
	logger.Printf("event: %s, details: %v", eventName, details)
	http.Error(w, "Authentication failed. Please close this window and try again.", http.StatusBadRequest)
}

// LoginHandler handles the OAuth callback from Spotify.
func LoginHandler(logger *log.Logger, apiCallbackURL string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		logger.Printf("event: callback.received, details: {method: %s, path: %s}", r.Method, r.URL.Path)

		// --- Input Validation ---
		code := r.URL.Query().Get("code")
		state := r.URL.Query().Get("state")
		errorParam := r.URL.Query().Get("error")

		if errorParam != "" {
			writeGenericError(w, logger, "callback.validation.failure", map[string]interface{}{"reason": "provider_error", "error": errorParam})
			return
		}

		if !paramValidator.MatchString(code) || code == "" {
			writeGenericError(w, logger, "callback.validation.failure", map[string]interface{}{"reason": "invalid_code_param"})
			return
		}

		if !paramValidator.MatchString(state) || state == "" {
			writeGenericError(w, logger, "callback.validation.failure", map[string]interface{}{"reason": "invalid_state_param"})
			return
		}

		// --- State & Nonce Validation ---
		if !validateState(state) {
			writeGenericError(w, logger, "callback.validation.failure", map[string]interface{}{"reason": "state_mismatch"})
			return
		}
		logger.Printf("event: callback.validation.success, details: {state_len: %d}", len(state))

		// --- Secret Handling & Handoff ---
		// The 'code' is sensitive and should not be logged. We log its length as a proxy.
		logger.Printf("event: callback.handoff.started, details: {code_len: %d}", len(code))

		body, err := json.Marshal(map[string]string{
			"code":  code,
			"state": state,
		})
		if err != nil {
			writeGenericError(w, logger, "callback.handoff.failure", map[string]interface{}{"reason": "json_marshal_error", "error": err.Error()})
			return
		}

		resp, err := http.Post(apiCallbackURL, "application/json", bytes.NewBuffer(body))
		if err != nil {
			writeGenericError(w, logger, "callback.handoff.failure", map[string]interface{}{"reason": "post_request_error", "error": err.Error()})
			return
		}
		defer resp.Body.Close()

		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			writeGenericError(w, logger, "callback.handoff.failure", map[string]interface{}{"reason": "read_response_error", "error": err.Error()})
			return
		}

		if resp.StatusCode >= 400 {
			logger.Printf("event: callback.handoff.failure, details: {status_code: %d, response: %s}", resp.StatusCode, string(respBody))
			// Return the backend's error page, but don't leak the raw response if it's not HTML/JSON
			w.WriteHeader(resp.StatusCode)
			fmt.Fprintln(w, "Authentication failed on the backend server.")
			return
		}

		logger.Printf("event: callback.handoff.success, details: {status_code: %d}", resp.StatusCode)
		w.WriteHeader(resp.StatusCode)
		w.Write(respBody)
	}
}
