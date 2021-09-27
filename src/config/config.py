from decouple import config

#get .env vars
SCRIPT_TEMPLATES = config("SCRIPT_TEMPLATES")
VPN_PORT = config("VPN_PORT")
VPN_PROTO = config("VPN_PROTO")
VPN_HOST = config("VPN_HOST")