FROM kylemanna/openvpn

COPY ./scripts/* ./

CMD ["ovpn_run"]