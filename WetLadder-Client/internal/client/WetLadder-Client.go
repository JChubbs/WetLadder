package main

import ( 
	"fmt"
	"os/exec"
	"os"

	"WetLadder-Client/internal/config"
)

func main() {
	fmt.Println("Starting WetLadder-Client!")

	fmt.Println("Retrieving .env config")
	config, err := config.GetConfig()
	if err != nil {
		fmt.Println("Bad Config")
		return
	}

	if _, err := os.Stat(config.ExecutablePath); err != nil {
		fmt.Printf("Executable file does not exist! %s\n", config.ExecutablePath)
	}

	if _, err := os.Stat(config.OpenVPNConfig); err != nil {
		fmt.Printf("OpenVPN Config file does not exist! %s\n", config.OpenVPNConfig)
	}

	fmt.Printf("Running OpenVPN @ %s config %s\n", config.ExecutablePath, config.OpenVPNConfig)
	cmd := exec.Command(config.ExecutablePath, "--config", config.OpenVPNConfig)
	/*
	if err := cmd.Run(); err != nil {
		fmt.Println("Error: ", err)
	}
	*/
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("%s\n", out)
	for {

	}
}