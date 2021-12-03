package main

import ( 
	"fmt"
	"os/exec"
	"os"

	"WetLadder-Client/internal/config"
	"WetLadder-Client/internal/obfuscator"
)

func main() {
	fmt.Println("Starting WetLadder-Client!")

	fmt.Println("Retrieving .env config")
	config, err := config.GetConfig()
	if err != nil {
		fmt.Println("Bad Config")
		return
	}

	//ensure ovpn file exists
	if _, err := os.Stat(config.OpenVPNConfig); err != nil {
		fmt.Printf("OpenVPN config file does not exist! %s\n", config.OpenVPNConfig)
		return
	}

	//obfuscation configured?
	obfuscator, err := obfuscator.GetObfuscator(config)
	if err != nil {
		fmt.Printf("Failed to get obfuscation configuration %s\n", err)
		return
	}

	if obfuscator != nil {
		fmt.Println("Starting obfuscator!")
		err := obfuscator.Start()
		if err != nil {
			fmt.Printf("Encountered an error when starting the obfuscator! %s\n", err)
			return
		}
	}

	if _, err := os.Stat(config.ExecutablePath); err != nil {
		fmt.Printf("Executable file does not exist! %s\n", config.ExecutablePath)
		return
	}

	if _, err := os.Stat(config.OpenVPNConfig); err != nil {
		fmt.Printf("OpenVPN Config file does not exist! %s\n", config.OpenVPNConfig)
		return
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
		return
	}
	fmt.Printf("%s\n", out)
	for {

	}
}