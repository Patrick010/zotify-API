package listener

import (
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestLoginHandler(t *testing.T) {
	// Create a new logger that discards output.
	logger := log.New(io.Discard, "", 0)

	// Create a new test server that will act as the backend API.
	backend := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))
	defer backend.Close()

	// Create a new test request for the Snitch listener.
	req := httptest.NewRequest("GET", "/login?code=123&state=456", nil)
	// Create a new response recorder.
	rr := httptest.NewRecorder()

	// Create a new handler for the Snitch listener.
	handler := LoginHandler(logger, backend.URL)
	// Serve the request.
	handler.ServeHTTP(rr, req)

	// Check the status code.
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Check the response body.
	expected := `OK`
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v",
			rr.Body.String(), expected)
	}
}
