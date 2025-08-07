package listener

import (
	"context"
	"log"
	"net/http"
	"time"
)

const (
	listenAddr    = "localhost:21371"
	serverTimeout = 2 * time.Minute
)

// Start initializes and runs the HTTP listener. It sets up a server on
// localhost:21371 that waits for a single callback to the /callback endpoint.
// The server will gracefully shut down after a valid request is received (with
// the correct state token) or after a 2-minute timeout.
//
// expectedState is the required value for the 'state' query parameter for the
// request to be considered valid.
func Start(expectedState string) {
	shutdown := make(chan bool, 1)

	mux := http.NewServeMux()
	mux.HandleFunc("/callback", newHandler(shutdown, expectedState))

	server := &http.Server{
		Addr:    listenAddr,
		Handler: mux,
	}

	// Goroutine to listen for shutdown signal
	go func() {
		<-shutdown
		log.Println("Shutdown signal received, stopping listener...")
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		if err := server.Shutdown(ctx); err != nil {
			log.Printf("Graceful shutdown failed: %v", err)
		}
	}()

	// Goroutine for timeout
	go func() {
		time.Sleep(serverTimeout)
		log.Println("Timeout reached. Shutting down listener.")
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		if err := server.Shutdown(ctx); err != nil {
			log.Printf("Graceful shutdown after timeout failed: %v", err)
		}
	}()

	log.Printf("Snitch is listening on http://%s/callback", listenAddr)
	log.Println("Waiting for Spotify to redirect... The listener will time out in 2 minutes.")

	if err := server.ListenAndServe(); err != http.ErrServerClosed {
		log.Fatalf("Listener error: %v", err)
	}

	log.Println("Snitch has shut down.")
}
