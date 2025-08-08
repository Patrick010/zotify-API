package main

import (
	"flag"
	"log"
	"zotify-api/snitch/internal/listener"
)

func main() {
	state := flag.String("state", "", "The state token for OAuth validation.")
	ipcToken := flag.String("ipc-token", "", "The token for authenticating with the Zotify API IPC server.")
	ipcPort := flag.Int("ipc-port", 0, "The port for the Zotify API IPC server.")
	flag.Parse()

	if *state == "" {
		log.Fatalln("Error: The -state flag is required.")
	}
	if *ipcToken == "" {
		log.Fatalln("Error: The -ipc-token flag is required.")
	}
	if *ipcPort == 0 {
		log.Fatalln("Error: The -ipc-port flag is required.")
	}

	listener.Start(*state, *ipcToken, *ipcPort)
}
