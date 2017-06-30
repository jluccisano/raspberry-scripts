package main

import (
   "os/exec"
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
	
	rest.HandleGET("/get", func(params url.Values) (string, error) {
		v := params.Get("relay")
		if v == "" {
			return nil, errors.New("Expecting GET parameter 'relay'")
		}
		cmd := exec.Command("python",  "relay_control.py", "get", "--relay 1")
		fmt.Println(cmd.Args)
		out, err := cmd.CombinedOutput()
		if err != nil { fmt.Println(err); }
		fmt.Println(string(out))
		return "value = " + string(out), nil
	})

        rest.RunServer("0.0.0.0:8080", stopServerChan)

}
