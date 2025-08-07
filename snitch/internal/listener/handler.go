package listener

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// oAuthPayload defines the structure of the incoming JSON payload.
type oAuthPayload struct {
	Code  string `json:"code"`
	State string `json:"state"`
}

// newHandler creates a new HTTP handler for the /snitch/oauth-code endpoint.
// It validates POST requests, parses the JSON payload, and checks the state token.
func newHandler(shutdown chan<- bool, expectedState string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 1. Validate Method
		if r.Method != http.MethodPost {
			http.Error(w, "Error: Method not allowed. Only POST requests are accepted.", http.StatusMethodNotAllowed)
			log.Printf("Rejected non-POST request from %s", r.RemoteAddr)
			return
		}

		// 2. Decode JSON payload
		var payload oAuthPayload
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			http.Error(w, "Error: Malformed JSON in request body.", http.StatusBadRequest)
			log.Printf("Failed to decode JSON from %s: %v", r.RemoteAddr, err)
			return
		}

		// 3. Validate State
		if payload.State == "" {
			http.Error(w, "Error: 'state' field is missing from JSON payload.", http.StatusBadRequest)
			log.Printf("Rejected request from %s due to missing state.", r.RemoteAddr)
			return
		}
		if payload.State != expectedState {
			http.Error(w, "Error: Invalid state token.", http.StatusBadRequest)
			log.Printf("Rejected request from %s due to invalid state. Expected: %s, Got: %s", r.RemoteAddr, expectedState, payload.State)
			return
		}

		// 4. Validate Code
		if payload.Code == "" {
			http.Error(w, "Error: 'code' field is missing from JSON payload.", http.StatusBadRequest)
			log.Printf("Rejected request from %s due to missing code.", r.RemoteAddr)
			return
		}

		// 5. Success: Print code and shut down
		log.Printf("Successfully received and validated OAuth code from %s.", r.RemoteAddr)
		fmt.Println(payload.Code)

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})

		shutdown <- true
	}
}
