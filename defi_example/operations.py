# pylint: disable=E0401
"""The main module with the class MetamaskOperation to make the possible operations"""
import requests
import json
from constants import WEI
from utils import CryptoUtils, get_api_key
from methods import WebThreeMethods, MethodBlocks
from networks import CryptoNetwork


class MetamaskOperation:
    """Class contains all neccesary methods for using with Metamask"""
    def __init__(self, wallet):
        self.wallet = wallet
        self.api_key = get_api_key()
        self.headers = {"content-type": "application/json"}
        self.block = MethodBlocks().latest
        self.net_url = CryptoNetwork().BNB
        self.url = f"{self.net_url}{self.api_key}"

    def _requested_payload(self, operation, *param_args):
        params = list(param_args)
        return {
            "jsonrpc": "2.0",
            "method": operation,
            "params": params,
            "id": 1
        }

    def _etherium_price(self):
        return CryptoUtils("ETH").get_price()

    def _response_from_request(self, payload):
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()

    def _response_to_usd(self, response):
        return int(response.get('result', 0.0), 16) * WEI * float(self._etherium_price())

    def _response_to_num(self, response):
        return int(response.get('result', 0.0), 16)

    def _usd(self, payload):
        return self._response_to_usd(self._response_from_request(payload))

    def _num(self, payload):
        return self._response_to_num(self._response_from_request(payload))

    def get_balance(self):
        """Method return the balance of the current Metamask network address"""
        payload = self._requested_payload(WebThreeMethods().get_balance, self.wallet, self.block)
        return self._usd(payload)

    def get_gas_price(self):
        """return current gas for transaction"""
        payload = self._requested_payload(WebThreeMethods().gas_price)
        return self._usd(payload)

    def get_transaction_count(self):
        """return wallet transaction count"""
        payload = self._requested_payload(WebThreeMethods().get_transaction_count,
                                          self.wallet, self.block)
        return self._num(payload)

    def chain_id(self):
        """return chain id"""
        payload = self._requested_payload(WebThreeMethods().chan_id)
        return self._num(payload)

    def max_priority_fee_per_gas(self):
        """Returns an estimate of how much priority fee, in wei, you need to be
        included in a block."""
        payload = self._requested_payload(WebThreeMethods().max_priority_fee_per_gas)
        return self._num(payload)

    def accounts(self):
        """Returns a list of addresses owned by the client."""
        payload = self._requested_payload(WebThreeMethods().accounts)
        return self._response_from_request(payload).get('result', 1)

    def listening(self):
        """Returns true if client is actively listening for network connections."""
        payload = self._requested_payload(WebThreeMethods().listen)
        return self._response_from_request(payload).get('result', 'True')

    def peer_nums(self):
        """Returns the number of peers currently connected to the client."""
        payload = self._requested_payload(WebThreeMethods().peer_nums)
        return self._num(payload)
