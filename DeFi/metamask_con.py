import requests
import json
from constants import WEI, BASE_URL


address = "0x107119102c2EC84099cDce3D5eFDE2dcbf4DEB2a"
# possible blocks vals: latest, earliest, pending, safe, or finalized
block = "latest"

payload = {
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": [address, block],
    "id": 1
}

headers = {"content-type": "application/json"}


def get_api_key():
    with open('mm_api_key', 'r') as api_key_file:
        api_key = api_key_file.read()
    return api_key


def get_balance():
    etherium = 2041.46
    url = f"{BASE_URL}{get_api_key()}"
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    print(response)
    balance = int(response['result'], 16) * WEI * etherium
    print(f"Balance: {balance}")


get_balance()
