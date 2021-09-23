
ovpn_data:=ovpn_data

setup:
	docker volume rm ${ovpn_data}
	docker volume create --name ${ovpn_data}
	docker build -t wet_ladder .
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder ovpn_genconfig -u udp://localhost:1194
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder /bin/bash /initpki.sh

create_client:
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder /bin/bash /build_client.sh $(client_name)

delete_client:
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder /bin/bash /delete_client.sh $(client_name)

get_client:
	docker run -v ${ovpn_data}:/etc/openvpn --rm wet_ladder ovpn_getclient $(client_name) > $(client_name).ovpn

run_vpn:
	docker run -v ${ovpn_data}:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN wet_ladder