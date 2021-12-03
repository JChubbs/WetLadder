package config

import ( 
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
)

type Config struct {
	ExecutablePath string `envconfig:"EXECUTABLE_PATH"`
	OpenVPNConfig  string `envconfig:"OPENVPN_CONFIG"`
	Platform 	   string `envconfig:"PLATFORM"`

	ObfuscationType string `envconfig:"OBFUSCATION_TYPE"`
	ObfuscationTarget string `envconfig:"OBFUSCATION_TARGET"`
	ObfuscatorPath string `envconfig:"OBFUSCATOR_PATH"`
}

func GetConfig() (Config, error) {

	if _, err := os.Stat(".env"); err == nil {
		err = godotenv.Load()
		if err != nil {
			fmt.Println("Error loading .env file")
		}
	}

	var config Config
	err := envconfig.Process("", &config)
	if err != nil {
		fmt.Println("Error loading .env file")
		return Config{}, err
	}

	return config, nil
}