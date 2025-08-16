package listener

import (
	"log"
	"net/http"
)

// Server is the HTTP server for the Snitch listener.
type Server struct {
	// Port is the port for the Snitch listener.
	Port string
	// Logger is the logger for the Snitch listener.
	Logger *log.Logger
}

// NewServer creates a new Server instance.
func NewServer(port string, logger *log.Logger) *Server {
	return &Server{
		Port:   port,
		Logger: logger,
	}
}

// Run starts the Snitch listener.
func (s *Server) Run(handler http.Handler) {
	addr := "127.0.0.1:" + s.Port
	s.Logger.Printf("Listening on http://%s", addr)
	s.Logger.Fatal(http.ListenAndServe(addr, handler))
}
