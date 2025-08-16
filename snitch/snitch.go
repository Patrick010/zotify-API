package snitch

import (
	"bytes"
	"encoding/json"
	"github.com/Patrick010/zotify-API/snitch/internal/listener"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

// Snitch is a short-lived, local OAuth callback HTTP listener.
// It is a subproject of Zotify-API.

// The primary purpose of Snitch is to solve the Spotify authentication
// redirect problem for headless or CLI-based Zotify-API usage. When a
// user needs to authenticate with Spotify, they are redirected to a URL.
// Snitch runs a temporary local web server on `localhost:4381` to catch
// this redirect, extract the authentication `code` and `state`, and
// securely forward them to the main Zotify API backend.

// Snitch is intended to be run as a standalone process during the
// authentication flow. It is configured via an environment variable.

// When started, Snitch listens on `http://localhost:4381/login`. After
// receiving a callback from Spotify, it will make a `POST` request with
// a JSON body (`{"code": "...", "state": "..."}`) to the configured
// callback URL.

const (
	// DefaultPort is the default port for the Snitch listener.
	DefaultPort = "4381"
)

// Config holds the configuration for the Snitch listener.
type Config struct {
	// Port is the port for the Snitch listener.
	Port string
	// APICallbackURL is the URL of the backend API's callback endpoint.
	APICallbackURL string
}

// App is the main application for the Snitch listener.
type App struct {
	// Config is the configuration for the Snitch listener.
	Config *Config
	// Logger is the logger for the Snitch listener.
	Logger *log.Logger
}

// NewApp creates a new App instance.
func NewApp(config *Config, logger *log.Logger) *App {
	return &App{
		Config: config,
		Logger: logger,
	}
}

// Run starts the Snitch listener.
func (a *App) Run() {
	server := listener.NewServer(a.Config.Port, a.Logger)
	handler := listener.LoginHandler(a.Logger, a.Config.APICallbackURL)
	server.Run(handler)
}

// loginHandler handles the OAuth callback from Spotify.
func (a *App) loginHandler(w http.ResponseWriter, r *http.Request) {
	// Extract the `code` and `state` from the query parameters.
	code := r.URL.Query().Get("code")
	state := r.URL.Query().Get("state")

	// Create the JSON body for the POST request.
	body, err := json.Marshal(map[string]string{
		"code":  code,
		"state": state,
	})
	if err != nil {
		a.Logger.Printf("Error marshalling JSON: %v", err)
		http.Error(w, "Error marshalling JSON", http.StatusInternalServerError)
		return
	}

	// Make the POST request to the backend API's callback endpoint.
	resp, err := http.Post(a.Config.APICallbackURL, "application/json", bytes.NewBuffer(body))
	if err != nil {
		a.Logger.Printf("Error making POST request: %v", err)
		http.Error(w, "Error making POST request", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Read the response body from the backend API.
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		a.Logger.Printf("Error reading response body: %v", err)
		http.Error(w, "Error reading response body", http.StatusInternalServerError)
		return
	}

	// Write the response from the backend API to the Snitch listener's response.
	w.WriteHeader(resp.StatusCode)
	w.Write(respBody)
}

// GetEnv returns the value of an environment variable or a default value.
func GetEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}

// GetRequiredEnv returns the value of an environment variable or panics if it is not set.
func GetRequiredEnv(key string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	panic(fmt.Sprintf("Required environment variable %s is not set", key))
}

// GetLogger returns a new logger instance.
func GetLogger(prefix string) *log.Logger {
	return log.New(os.Stdout, strings.ToUpper(prefix)+": ", log.Ldate|log.Ltime|log.Lshortfile)
}
