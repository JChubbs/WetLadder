
setup:
	yum install git docker golang -y
	cd shapeshifter-dispatcher; go build
	python3 -m pip install -r ./requirements.txt
	alembic upgrade head
	systemctl start docker