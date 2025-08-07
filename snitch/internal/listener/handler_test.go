package listener

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestNewHandler(t *testing.T) {
	const expectedState = "secret-test-state"

	testCases := []struct {
		name               string
		method             string
		body               string
		expectedStatusCode int
		expectShutdown     bool
	}{
		{
			name:               "Valid Request",
			method:             http.MethodPost,
			body:               `{"code": "test-code", "state": "secret-test-state"}`,
			expectedStatusCode: http.StatusOK,
			expectShutdown:     true,
		},
		{
			name:               "Invalid State",
			method:             http.MethodPost,
			body:               `{"code": "test-code", "state": "wrong-state"}`,
			expectedStatusCode: http.StatusBadRequest,
			expectShutdown:     false,
		},
		{
			name:               "Missing State",
			method:             http.MethodPost,
			body:               `{"code": "test-code"}`,
			expectedStatusCode: http.StatusBadRequest,
			expectShutdown:     false,
		},
		{
			name:               "Missing Code",
			method:             http.MethodPost,
			body:               `{"state": "secret-test-state"}`,
			expectedStatusCode: http.StatusBadRequest,
			expectShutdown:     false,
		},
		{
			name:               "Malformed JSON",
			method:             http.MethodPost,
			body:               `{"code": "test-code", "state": "secret-test-state"`,
			expectedStatusCode: http.StatusBadRequest,
			expectShutdown:     false,
		},
		{
			name:               "Invalid Method GET",
			method:             http.MethodGet,
			body:               "",
			expectedStatusCode: http.StatusMethodNotAllowed,
			expectShutdown:     false,
		},
		{
			name:               "Invalid Method PUT",
			method:             http.MethodPut,
			body:               `{"code": "test-code", "state": "secret-test-state"}`,
			expectedStatusCode: http.StatusMethodNotAllowed,
			expectShutdown:     false,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			req := httptest.NewRequest(tc.method, "/snitch/oauth-code", bytes.NewBufferString(tc.body))
			rr := httptest.NewRecorder()
			shutdownChan := make(chan bool, 1)

			handler := newHandler(shutdownChan, expectedState)
			handler.ServeHTTP(rr, req)

			if rr.Code != tc.expectedStatusCode {
				t.Errorf("expected status code %d, got %d", tc.expectedStatusCode, rr.Code)
			}

			// Check if shutdown was signaled
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

			// For the valid case, check the body
			if tc.expectedStatusCode == http.StatusOK {
				if !strings.Contains(rr.Body.String(), `"status":"ok"`) {
					t.Errorf("expected response body to contain `{\"status\":\"ok\"}`, got `%s`", rr.Body.String())
				}
			}
		})
	}
}
