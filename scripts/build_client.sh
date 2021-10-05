#!/bin/bash

easyrsa build-client-full $2 nopass <<finish
$1
finish