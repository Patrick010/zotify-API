package listener

import (
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// mockBackendServer creates a test server to act as the FastAPI backend.
func mockBackendServer(t *testing.T, expectedCode, expectedState string) *httptest.Server {
	handler := func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			t.Errorf("Backend received wrong method. Got %s, want POST", r.Method)
			http.Error(w, "Bad Method", http.StatusMethodNotAllowed)
			return
		}

		body, _ := io.ReadAll(r.Body)
		expectedBody := `{"code":"` + expectedCode + `","state":"` + expectedState + `"}`
		if strings.TrimSpace(string(body)) != expectedBody {
			t.Errorf("Backend received wrong body. Got %s, want %s", string(body), expectedBody)
			http.Error(w, "Bad Request", http.StatusBadRequest)
			return
		}
		w.WriteHeader(http.StatusOK)
	}
	return httptest.NewServer(http.HandlerFunc(handler))
}

func TestHandleCallback(t *testing.T) {
	// This test is more limited now, as the handler function is not passed dependencies.
	// We can't easily mock the backend URL. The user's example code hardcodes it,
	// so for this test, we'll assume the hardcoded URL is unreachable and test that path.
	// A more advanced implementation would inject the backend URL as a dependency.

	t.Run("Missing Code Parameter", func(t *testing.T) {
		req := httptest.NewRequest("GET", "/login?state=somestate", nil)
		rr := httptest.NewRecorder()
		handleCallback(rr, req)

		if rr.Code != http.StatusBadRequest {
			t.Errorf("expected status code %d, got %d", http.StatusBadRequest, rr.Code)
		}
		if !strings.Contains(rr.Body.String(), "parameter was missing") {
			t.Errorf("expected error message about missing params, got: %s", rr.Body.String())
		}
	})

	t.Run("Missing State Parameter", func(t *testing.T) {
		req := httptest.NewRequest("GET", "/login?code=somecode", nil)
		rr := httptest.NewRecorder()
		handleCallback(rr, req)

		if rr.Code != http.StatusBadRequest {
			t.Errorf("expected status code %d, got %d", http.StatusBadRequest, rr.Code)
		}
	})

	t.Run("Forwarding Failure", func(t *testing.T) {
		// This test assumes the hardcoded backend URL is not available,
		// which will be true during isolated unit testing.
		req := httptest.NewRequest("GET", "/login?code=somecode&state=somestate", nil)
		rr := httptest.NewRecorder()
		handleCallback(rr, req)

		if rr.Code != http.StatusInternalServerError {
			t.Errorf("expected status code %d, got %d", http.StatusInternalServerError, rr.Code)
		}
		if !strings.Contains(rr.Body.String(), "Could not connect to the application backend") {
			t.Errorf("expected error message about backend connection, got: %s", rr.Body.String())
		}
	})
}
