import requests
import json
from constants import WEI, BASE_URL
from utils import CryptoUtils, get_api_key
from methods import EtheriumMethods


class MetamaskOperation:
    def __init__(self, wallet):
        self.wallet = wallet
        self.api_key = get_api_key()
        self.headers = {"content-type": "application/json"}
        # possible blocks vals: latest, earliest, pending, safe, or finalized
        self.block = "latest"
        self.url = f"{BASE_URL}{self.api_key}"

    def requested_payload(self, operation, *param_args):
        params = [param for param in param_args]
        return {
            "jsonrpc": "2.0",
            "method": operation,
            "params": params,
            "id": 1
        }

    def etherium_price(self):
        return CryptoUtils("ETH").get_price()

    def response_from_request(self, payload):
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()

    def get_balance(self):
        payload = self.requested_payload(EtheriumMethods().get_balance, self.wallet, self.block)
        response = self.response_from_request(payload)
        return int(response.get('result', 0.0), 16) * WEI * float(self.etherium_price())

    def get_gas_price(self):
        payload = self.requested_payload(EtheriumMethods().gas_price)
        response = self.response_from_request(payload)
        return int(response.get('result', 0.0), 16) * WEI * float(self.etherium_price())

    def get_transaction_count(self):
        payload = self.requested_payload(EtheriumMethods().get_transaction_count, self.wallet, self.block)
        response = self.response_from_request(payload)
        return int(response.get('result', 0.0), 16)

    def chain_id(self):
        payload = self.requested_payload(EtheriumMethods().chan_id)
        response = self.response_from_request(payload)
        return int(response.get('result', 0.0), 16)

    def max_priority_fee_per_gas(self):
        payload = self.requested_payload(EtheriumMethods().max_priority_fee_per_gas)
        response = self.response_from_request(payload)
        return int(response.get('result', 0.0), 16)
