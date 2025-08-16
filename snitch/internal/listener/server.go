package listener

import (
	"log"
	"net/http"
)

// Server is the HTTP server for the Snitch listener.
type Server struct {
	// Addr is the address for the Snitch listener.
	Addr string
	// Logger is the logger for the Snitch listener.
	Logger *log.Logger
}

// NewServer creates a new Server instance.
func NewServer(addr string, logger *log.Logger) *Server {
	return &Server{
		Addr:   addr,
		Logger: logger,
	}
}

// Run starts the Snitch listener.
func (s *Server) Run(handler http.Handler) {
	s.Logger.Printf("Listening on http://localhost%s", s.Addr)
	s.Logger.Fatal(http.ListenAndServe(s.Addr, handler))
}
