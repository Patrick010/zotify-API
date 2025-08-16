package main

import (
	"log"
	"os"

	"github.com/Patrick010/zotify-API/snitch"
)

func main() {
	logger := snitch.GetLogger("snitch")

	config := &snitch.Config{
		Port:           snitch.GetEnv("SNITCH_PORT", snitch.DefaultPort),
		APICallbackURL: snitch.GetRequiredEnv("SNITCH_API_CALLBACK_URL"),
	}

	app := snitch.NewApp(config, logger)
	app.Run()
}

// GetEnv returns the value of an environment variable or a default value.
func GetEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}

// GetRequiredEnv returns the value of an environment variable or panics if it is not set.
func GetRequiredEnv(key string) (string, error) {
	if value, ok := os.LookupEnv(key); ok {
		return value, nil
	}
	return "", log.New(os.Stderr, "ERROR: ", 0).Output(2, key+" is not set")
}
