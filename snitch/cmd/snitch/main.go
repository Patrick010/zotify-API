package main

import (
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
