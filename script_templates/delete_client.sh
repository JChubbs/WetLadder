#!/bin/bash

rm /etc/openvpn/pki/reqs/$1.req
rm /etc/openvpn/pki/private/$1.key
rm /etc/openvpn/pki/issued/$1.crt