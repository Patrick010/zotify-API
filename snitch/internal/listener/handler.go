package listener

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
)

// LoginHandler handles the OAuth callback from Spotify.
func LoginHandler(logger *log.Logger, apiCallbackURL string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Extract the `code` and `state` from the query parameters.
		code := r.URL.Query().Get("code")
		state := r.URL.Query().Get("state")

		// Create the JSON body for the POST request.
		body, err := json.Marshal(map[string]string{
			"code":  code,
			"state": state,
		})
		if err != nil {
			logger.Printf("Error marshalling JSON: %v", err)
			http.Error(w, "Error marshalling JSON", http.StatusInternalServerError)
			return
		}

		// Make the POST request to the backend API's callback endpoint.
		resp, err := http.Post(apiCallbackURL, "application/json", bytes.NewBuffer(body))
		if err != nil {
			logger.Printf("Error making POST request: %v", err)
			http.Error(w, "Error making POST request", http.StatusInternalServerError)
			return
		}
		defer resp.Body.Close()

		// Read the response body from the backend API.
		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			logger.Printf("Error reading response body: %v", err)
			http.Error(w, "Error reading response body", http.StatusInternalServerError)
			return
		}

		// Write the response from the backend API to the Snitch listener's response.
		w.WriteHeader(resp.StatusCode)
		w.Write(respBody)
	}
}
