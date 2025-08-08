package listener

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// mockIPCServer creates a test server to act as the Zotify API backend.
func mockIPCServer(t *testing.T, expectedToken, expectedCode string) *httptest.Server {
	handler := func(w http.ResponseWriter, r *http.Request) {
		// Check token
		authHeader := r.Header.Get("Authorization")
		expectedHeader := "Bearer " + expectedToken
		if authHeader != expectedHeader {
			t.Errorf("IPC server received wrong token. Got %s, want %s", authHeader, expectedHeader)
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}

		// Check code
		body, _ := io.ReadAll(r.Body)
		if !strings.Contains(string(body), fmt.Sprintf(`"code":"%s"`, expectedCode)) {
			t.Errorf("IPC server received wrong code. Got %s, want %s", string(body), expectedCode)
			http.Error(w, "Bad Request", http.StatusBadRequest)
			return
		}

		w.WriteHeader(http.StatusOK)
	}
	return httptest.NewServer(http.HandlerFunc(handler))
}

func TestNewHandler_IPC(t *testing.T) {
	const expectedState = "secret-state"
	const expectedCode = "good-code"
	const ipcToken = "secret-ipc-token"

	// Start a mock server to act as the Zotify API backend
	server := mockIPCServer(t, ipcToken, expectedCode)
	defer server.Close()

	// Extract the port from the mock server's URL
	var ipcPort int
	fmt.Sscanf(server.URL, "http://127.0.0.1:%d", &ipcPort)

	testCases := []struct {
		name               string
		targetURL          string
		expectedStatusCode int
		expectShutdown     bool
	}{
		{
			name:               "Valid Request",
			targetURL:          fmt.Sprintf("/callback?code=%s&state=%s", expectedCode, expectedState),
			expectedStatusCode: http.StatusOK,
			expectShutdown:     true,
		},
		{
			name:               "Invalid State",
			targetURL:          fmt.Sprintf("/callback?code=%s&state=wrong-state", expectedCode),
			expectedStatusCode: http.StatusBadRequest,
			expectShutdown:     false,
		},
		{
			name:               "Missing Code",
			targetURL:          fmt.Sprintf("/callback?state=%s", expectedState),
			expectedStatusCode: http.StatusBadRequest,
			expectShutdown:     true, // Shutdown is triggered even on failure to prevent reuse
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			req := httptest.NewRequest("GET", tc.targetURL, nil)
			rr := httptest.NewRecorder()
			shutdownChan := make(chan bool, 1)

			handler := newHandler(shutdownChan, expectedState, ipcToken, ipcPort)
			handler.ServeHTTP(rr, req)

			if rr.Code != tc.expectedStatusCode {
				t.Errorf("expected status code %d, got %d", tc.expectedStatusCode, rr.Code)
			}

			select {
			case <-shutdownChan:
				if !tc.expectShutdown {
					t.Error("expected no shutdown signal, but got one")
				}
			default:
				if tc.expectShutdown {
					t.Error("expected shutdown signal, but got none")
				}
			}
		})
	}
}
