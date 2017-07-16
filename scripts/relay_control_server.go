package main

import (
	"fmt"
	"github.com/ungerik/go-rest"
	"net/url"
	"os/exec"
)

func main() {
	// See RunServer below
	stopServerChan := make(chan struct{})

	fmt.Printf("Starting REST server\n")

	rest.HandleGET("/get", func(in url.Values)  string {
		args := []string{"get"}
		fmt.Println(in)
		if in.Get("relay") != "" {
                        args = append(args,"--relay")
			args = append(args,(fmt.Sprintf("%s", in.Get("relay"))))
		}
		fmt.Println(args)
		cmd := exec.Command("./relay_control.py", args...)
		out, err := cmd.Output()

		if err != nil {
			println(err.Error())
			return ""
		}

		return fmt.Sprintf(string(out))
	})

	rest.HandlePOST("/set", func(in url.Values)  string {
		if in.Get("state") == "" {
			println("State param is mandatory.")
			return ""
		}
		fmt.Println(in)
		args := []string{"set","--state", fmt.Sprintf("%s", in.Get("state"))}
		if in.Get("relay") != "" {
			args = append(args,"--relay")
			args = append(args, fmt.Sprintf("%s", in.Get("relay")))
		}
		fmt.Println(args)
		cmd := exec.Command("./relay_control.py", args...)
		out, err := cmd.Output()

		if err != nil {
			println(err.Error())
			return ""
		}

		return fmt.Sprintf(string(out))
	})

	rest.HandleGET("/close", func() string {
		stopServerChan <- struct{}{}
		return "Stopping REST server..."
	})

	rest.RunServer("0.0.0.0:8080", stopServerChan)
}
