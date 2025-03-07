import requests
import json
from constants import WEI, BASE_URL
from utils import CryptoUtils, get_api_key


class MetamaskOperation:
    def __init__(self, wallet, operation):
        self.wallet = wallet
        self.api_key = get_api_key()
        self.operation = operation
        self.headers = {"content-type": "application/json"}
        # possible blocks vals: latest, earliest, pending, safe, or finalized
        self.block = "latest"

    def requested_payload(self):
        return {
            "jsonrpc": "2.0",
            "method": self.operation,
            "params": [self.wallet, self.block],
            "id": 1
        }

    def etherium_price(self):
        return CryptoUtils("ETH").get_price()

    def get_balance(self):
        url = f"{BASE_URL}{self.api_key}"
        payload = self.requested_payload()
        response = requests.post(url, data=json.dumps(payload), headers=self.headers).json()
        balance = int(response['result'], 16) * WEI * float(self.etherium_price())
        return balance
