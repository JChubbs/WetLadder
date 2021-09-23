#!/bin/bash

easyrsa build-client-full $1 nopass <<finish
ca_key_passphrase
finish