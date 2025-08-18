package snitch

import (
	"log"
	"net/http"
	"os"
	"time"

	"github.com/Patrick010/zotify-API/snitch/internal/listener"
)

const DefaultPort = "4381"

// --- Config ---

type Config struct {
	Port           string
	APICallbackURL string
}

func GetEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func GetRequiredEnv(key string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	log.Fatalf("FATAL: Required environment variable %s is not set", key)
	return "" // Unreachable
}

// --- Logger ---

func GetLogger(name string) *log.Logger {
	return log.New(os.Stdout, name+": ", log.Ldate|log.Ltime|log.Lshortfile)
}

// --- App ---

type App struct {
	config *Config
	logger *log.Logger
}

func NewApp(config *Config, logger *log.Logger) *App {
	return &App{
		config: config,
		logger: logger,
	}
}

func (a *App) Run() {
	listenAddr := "127.0.0.1:" + a.config.Port
	a.logger.Println("Starting snitch on", listenAddr)

	// Use the new, correct handler from the listener package
	http.HandleFunc("/login", listener.LoginHandler(a.logger, a.config.APICallbackURL))

	server := &http.Server{
		Addr:         listenAddr,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  15 * time.Second,
	}

	if err := server.ListenAndServe(); err != nil {
		a.logger.Fatalf("Could not start server: %s\n", err)
	}
}
