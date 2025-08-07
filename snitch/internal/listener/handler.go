package listener

import (
	"fmt"
	"log"
	"net/http"
)

// newHandler creates a new HTTP handler for the /callback endpoint.
// It takes a channel to signal the server to shut down and the expected state token.
func newHandler(shutdown chan<- bool, expectedState string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		code := r.URL.Query().Get("code")
		state := r.URL.Query().Get("state")

		if state == "" {
			log.Println("OAuth callback received without a state token.")
			http.Error(w, "Error: Missing state token in callback.", http.StatusBadRequest)
			return
		}

		if state != expectedState {
			log.Printf("OAuth callback received with invalid state token. Expected: %s, Got: %s", expectedState, state)
			http.Error(w, "Error: Invalid state token.", http.StatusBadRequest)
			return
		}

		if code == "" {
			log.Println("OAuth callback received without a code.")
			http.Error(w, "Error: Missing authorization code in callback.", http.StatusBadRequest)
			return
		}

		// Print the code to standard output for the parent process to capture.
		fmt.Println(code)

		// Respond to the user's browser.
		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "Authentication successful! You can close this window now.")
		log.Printf("Successfully received OAuth code with valid state token.")

		// Signal the server to shut down.
		go func() {
			shutdown <- true
		}()
	}
}
