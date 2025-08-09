package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

const (
	listenAddr    = "localhost:4381"
	callbackPath  = "/login"
	defaultAPIURL = "http://192.168.20.5:8000/api/auth/spotify/callback"
)

type CallbackPayload struct {
	Code  string `json:"code"`
	State string `json:"state"`
}

func main() {
	apiURL := os.Getenv("SNITCH_API_CALLBACK_URL")
	if apiURL == "" {
		apiURL = defaultAPIURL
	}
	log.Printf("[INIT] Snitch starting on http://%s%s", listenAddr, callbackPath)
	log.Printf("[INFO] Forwarding callbacks to: %s", apiURL)

	http.HandleFunc(callbackPath, func(w http.ResponseWriter, r *http.Request) {
		log.Println("=== Incoming /callback request ===")

		if r.Method != http.MethodGet {
			log.Printf("[WARN] Invalid method: %s", r.Method)
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		code := r.URL.Query().Get("code")
		state := r.URL.Query().Get("state")

		if code == "" || state == "" {
			log.Println("[ERROR] Missing code or state")
			http.Error(w, "Missing 'code' or 'state' parameter", http.StatusBadRequest)
			return
		}

		log.Printf("[INFO] Code: %s", code)
		log.Printf("[INFO] State: %s", state)

		payload := CallbackPayload{Code: code, State: state}
		jsonBody, err := json.Marshal(payload)
		if err != nil {
			log.Printf("[ERROR] Failed to encode payload: %v", err)
			http.Error(w, "Internal error", http.StatusInternalServerError)
			return
		}

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err := client.Post(apiURL, "application/json", bytes.NewBuffer(jsonBody))
		if err != nil {
			log.Printf("[ERROR] POST failed: %v", err)
			http.Error(w, "Failed to notify backend", http.StatusBadGateway)
			return
		}
		defer resp.Body.Close()

		log.Printf("[INFO] Backend responded with: %s", resp.Status)
		if resp.StatusCode != http.StatusOK {
			log.Printf("[WARN] Non-200 response from backend")
		}

		fmt.Fprintln(w, "Authorization complete. You can close this window.")
		log.Println("=== Callback handling complete ===")
	})

	if err := http.ListenAndServe(listenAddr, nil); err != nil {
		log.Fatalf("[FATAL] Server failed: %v", err)
	}
}
