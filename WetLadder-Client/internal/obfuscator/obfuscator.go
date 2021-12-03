package obfuscator

import ( 
	"fmt"
	"os/exec"
	"os"

	"github.com/phayes/freeport"

	"WetLadder-Client/internal/config"
)

type Obfuscator struct {
	ObfuscationType string
	ObfuscationTarget string
	ObfuscatorPath string
	OpenVPNConfig string
}

func GetObfuscator(c config.Config) (*Obfuscator, error) {
	if c.ObfuscationType != "" && c.ObfuscationTarget != "" && c.ObfuscatorPath != "" {

		//ensure path exists
		if _, err := os.Stat(c.ExecutablePath); err != nil {
			fmt.Printf("Executable file does not exist! %s\n", c.ObfuscatorPath)
			return nil, err
		}

		return &Obfuscator{
			ObfuscationType: c.ObfuscationType,
			ObfuscationTarget: c.ObfuscationTarget,
			ObfuscatorPath: c.ObfuscatorPath,
			OpenVPNConfig: c.OpenVPNConfig,
		}, nil
	} else {
		return nil, nil
	}
}

func (o *Obfuscator) Start() error {
	//find an available port
	port, err := freeport.GetFreePort()
	if err != nil {
		return err
	}

	//alter config file to connect to localhost at new port
	f, err := os.OpenFile(o.OpenVPNConfig, os.O_APPEND|os.O_WRONLY, 0600)
	if err != nil {
		return err
	}
	defer f.Close()
	fmt.Fprintf(f, "%s", fmt.Sprintf("\nremote 127.0.0.1 %d tcp", port))
	
	cmd := exec.Command(
		fmt.Sprintf("./%s", o.ObfuscatorPath),
		"-transparent",
		"-client",
		"-state",
		"state",
		"-target", o.ObfuscationTarget,
		"-transports", o.ObfuscationType,
		"-proxylistenaddr", fmt.Sprintf("127.0.0.1:%d", port),
		"-ptversion", "2",
		"-logLevel", "DEBUG",
		"-enableLogging",
	)
	cmd.Start()

	return nil
}