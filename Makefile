
setup:
	yum install git -y
	yum install docker -y
	python3 -m pip install -r ./requirements.txt
	alembic upgrade head
	systemctl start docker