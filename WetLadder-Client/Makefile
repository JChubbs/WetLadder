
build_client:
	GOOS=windows GOARCH=386 go build -o client-builds/win-32/ internal/client/WetLadder-Client.go
	GOOS=windows GOARCH=amd64 go build -o client-builds/win-64/ internal/client/WetLadder-Client.go
	GOOS=darwin GOARCH=amd64 go build -o client-builds/mac/ internal/client/WetLadder-Client.go
	GOOS=linux GOARCH=386 go build -o client-builds/nix-32/ internal/client/WetLadder-Client.go
	GOOS=linux GOARCH=amd64 go build -o client-builds/nix-64/ internal/client/WetLadder-Client.go
	GOOS=linux GOARCH=arm go build -o client-builds/nix-arm/ internal/client/WetLadder-Client.go

build_shapeshifter:
	cd ../shapeshifter-dispatcher; GOOS=windows GOARCH=386 go build -o ../WetLadder-Client/shapeshifter-builds/win-32/
	cd ../shapeshifter-dispatcher; GOOS=windows GOARCH=amd64 go build -o ../WetLadder-Client/shapeshifter-builds/win-64/ 
	cd ../shapeshifter-dispatcher; GOOS=darwin GOARCH=amd64 go build -o ../WetLadder-Client/shapeshifter-builds/mac/ 
	cd ../shapeshifter-dispatcher; GOOS=linux GOARCH=386 go build -o ../WetLadder-Client/shapeshifter-builds/nix-32/ 
	cd ../shapeshifter-dispatcher; GOOS=linux GOARCH=amd64 go build -o ../WetLadder-Client/shapeshifter-builds/nix-64/ 
	cd ../shapeshifter-dispatcher; GOOS=linux GOARCH=arm go build -o ../WetLadder-Client/shapeshifter-builds/nix-arm/ 
	