
build:
	GOOS=windows GOARCH=386 go build -o client-builds/win-32/ internal/client/WetLadder-Client.go
	GOOS=windows GOARCH=amd64 go build -o client-builds/win-64/ internal/client/WetLadder-Client.go
	GOOS=darwin GOARCH=amd64 go build -o client-builds/mac/ internal/client/WetLadder-Client.go
	GOOS=linux GOARCH=386 go build -o client-builds/nix-32/ internal/client/WetLadder-Client.go
	GOOS=linux GOARCH=amd64 go build -o client-builds/nix-64/ internal/client/WetLadder-Client.go
	GOOS=linux GOARCH=arm go build -o client-builds/nix-arm/ internal/client/WetLadder-Client.go
	