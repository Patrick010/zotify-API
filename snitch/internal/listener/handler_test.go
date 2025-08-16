package listener

import (
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// setupTest creates a new logger and a mock backend API server for testing.
func setupTest() (*log.Logger, *httptest.Server) {
	logger := log.New(io.Discard, "", 0)
	backend := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))
	return logger, backend
}

func TestLoginHandler_Success(t *testing.T) {
	logger, backend := setupTest()
	defer backend.Close()

	req := httptest.NewRequest("GET", "/login?code=good-code&state=good-state", nil)
	rr := httptest.NewRecorder()

	handler := LoginHandler(logger, backend.URL)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	expected := `OK`
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v", rr.Body.String(), expected)
	}
}

func TestLoginHandler_MissingState(t *testing.T) {
	logger, backend := setupTest()
	defer backend.Close()

	req := httptest.NewRequest("GET", "/login?code=some-code", nil)
	rr := httptest.NewRecorder()

	handler := LoginHandler(logger, backend.URL)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing state: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestLoginHandler_MissingCode(t *testing.T) {
	logger, backend := setupTest()
	defer backend.Close()

	req := httptest.NewRequest("GET", "/login?state=some-state", nil)
	rr := httptest.NewRecorder()

	handler := LoginHandler(logger, backend.URL)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing code: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestLoginHandler_ProviderError(t *testing.T) {
	logger, backend := setupTest()
	defer backend.Close()

	req := httptest.NewRequest("GET", "/login?error=access_denied", nil)
	rr := httptest.NewRecorder()

	handler := LoginHandler(logger, backend.URL)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for provider error: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestLoginHandler_BackendError(t *testing.T) {
	backend := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Internal Server Error"))
	}))
	logger := log.New(io.Discard, "", 0)
	defer backend.Close()

	req := httptest.NewRequest("GET", "/login?code=good-code&state=good-state", nil)
	rr := httptest.NewRecorder()

	handler := LoginHandler(logger, backend.URL)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusInternalServerError {
		t.Errorf("handler returned wrong status code for backend error: got %v want %v", status, http.StatusInternalServerError)
	}

	if !strings.Contains(rr.Body.String(), "Authentication failed on the backend server") {
		t.Errorf("handler returned unexpected body for backend error: got %v", rr.Body.String())
	}
}
