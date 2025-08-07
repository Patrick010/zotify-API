package main

import (
	"flag"
	"log"
	"zotify-api/snitch/internal/listener"
)

func main() {
	state := flag.String("state", "", "The state token for OAuth validation.")
	flag.Parse()

	if *state == "" {
		log.Fatalln("Error: The -state flag is required.")
	}

	listener.Start(*state)
}
