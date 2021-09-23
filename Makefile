
ovpn_data:=ovpn_data

#connection details
address:=localhost
port:=1194
proto:=udp

setup:
	docker volume create --name ${ovpn_data}
	docker build -t wet_ladder .
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder ovpn_genconfig -u ${proto}://${address}:${port}
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder /bin/bash /initpki.sh

purge_old:
	docker container prune
	docker volume rm ${ovpn_data}

create_client:
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder /bin/bash /build_client.sh $(client_name)

delete_client:
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder /bin/bash /delete_client.sh $(client_name)

get_client:
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder ovpn_getclient $(client_name) > $(client_name).ovpn

run_vpn:
	docker run -v ${ovpn_data}:/etc/openvpn -d -p ${port}:${port}/${proto} --cap-add=NET_ADMIN wet_ladder