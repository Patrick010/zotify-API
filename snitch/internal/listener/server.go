package listener

import (
	"log"
	"net/http"
	"time"
)

const (
	listenAddr    = "127.0.0.1:4381"
	serverTimeout = 2 * time.Minute
	endpointPath  = "/login"
)

// Start initializes and runs the Snitch HTTP listener. It sets up a server on
// the fixed address 127.0.0.1:4381 and listens for a single GET request on the
// /login endpoint, as required by the Spotify application settings.
// The server will gracefully shut down after a request is handled.
func Start() {
	mux := http.NewServeMux()
	mux.HandleFunc(endpointPath, handleCallback)

	server := &http.Server{
		Addr:    listenAddr,
		Handler: mux,
	}

	log.Printf("Snitch listener running at http://%s%s ...", listenAddr, endpointPath)
	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Snitch server failed: %v\n", err)
	}
}
