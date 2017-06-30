package main

import (
   "fmt"
   "github.com/ungerik/go-rest"
)

func main() {
    fmt.Println("Hello, Arch!")

     rest.DontCheckRequestMethod = true
	rest.IndentJSON = "  "

	// See RunServer below
	stopServerChan := make(chan struct{})

	rest.HandleGET("/test", func() string {
		return "ici!"
	})

        rest.RunServer("0.0.0.0:8080", stopServerChan)

}
