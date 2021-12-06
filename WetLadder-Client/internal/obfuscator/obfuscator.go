package obfuscator

import ( 
	"fmt"
	"os/exec"
	"os"
	"io"

	"github.com/phayes/freeport"

	"WetLadder-Client/internal/config"
)

type Obfuscator struct {
	ObfuscationType string
	ObfuscationTarget string
	ObfuscatorPath string
	ObfuscatorConfigPath string
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
			ObfuscatorConfigPath: c.ObfuscatorConfigPath,
			OpenVPNConfig: c.OpenVPNConfig,
		}, nil
	} else {
		return nil, nil
	}
}

func (o *Obfuscator) Start() (string, error) {
	//find an available port
	port, err := freeport.GetFreePort()
	if err != nil {
		return "", err
	}

	//copy and alter config file to connect to localhost at new port
	outFileDest := fmt.Sprintf("%s-obfuscated.ovpn", o.OpenVPNConfig[:len(o.OpenVPNConfig)-5])
	
	source, err := os.Open(o.OpenVPNConfig)
    if err != nil {
            return "", err
    }
    defer source.Close()

    destination, err := os.Create(outFileDest)
    if err != nil {
            return "", err
    }
    defer destination.Close()

	_, err = io.Copy(destination, source)
	if err != nil {
		return "", err
	}

	f, err := os.OpenFile(outFileDest, os.O_APPEND|os.O_WRONLY, 0600)
	if err != nil {
		return "", err
	}
	defer f.Close()
	fmt.Fprintf(f, "%s", fmt.Sprintf("\nremote 127.0.0.1 %d tcp", port))
	
	args := []string{
		"-transparent",
		"-client",
		"-state", "state",
		"-target", o.ObfuscationTarget,
		"-transports", o.ObfuscationType,
		"-proxylistenaddr", fmt.Sprintf("127.0.0.1:%d", port),
		"-logLevel", "DEBUG",
		"-enableLogging",
	}

	//add method specific options
	if o.ObfuscationType == "obfs2" {
		args = append(args, "-ptversion", "2")
	} else if o.ObfuscationType == "obfs4" {
		args = append(args, "-optionsFile", o.ObfuscatorConfigPath)
	}

	cmd := exec.Command(
		fmt.Sprintf("./%s", o.ObfuscatorPath),
		args...
	)
	cmd.Start()

	return outFileDest, nil
}