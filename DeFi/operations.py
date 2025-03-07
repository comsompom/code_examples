import requests
import json
from constants import WEI
from utils import CryptoUtils, get_api_key
from methods import WebThreeMethods
from networks import CryptoNetwork


class MetamaskOperation:
    def __init__(self, wallet):
        self.wallet = wallet
        self.api_key = get_api_key()
        self.headers = {"content-type": "application/json"}
        # possible blocks vals: latest, earliest, pending, safe, or finalized
        self.block = "latest"
        bnb_url = CryptoNetwork().BNB
        self.url = f"{bnb_url}{self.api_key}"

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

    def response_to_usd(self, response):
        return int(response.get('result', 0.0), 16) * WEI * float(self.etherium_price())

    def response_to_num(self, response):
        return int(response.get('result', 0.0), 16)

    def get_balance(self):
        payload = self.requested_payload(WebThreeMethods().get_balance, self.wallet, self.block)
        return self.response_to_usd(self.response_from_request(payload))

    def get_gas_price(self):
        payload = self.requested_payload(WebThreeMethods().gas_price)
        return self.response_to_usd(self.response_from_request(payload))

    def get_transaction_count(self):
        payload = self.requested_payload(WebThreeMethods().get_transaction_count, self.wallet, self.block)
        return self.response_to_num(self.response_from_request(payload))

    def chain_id(self):
        payload = self.requested_payload(WebThreeMethods().chan_id)
        return self.response_to_num(self.response_from_request(payload))

    def max_priority_fee_per_gas(self):
        payload = self.requested_payload(WebThreeMethods().max_priority_fee_per_gas)
        return self.response_to_num(self.response_from_request(payload))
