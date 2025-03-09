# pylint: disable=E0401
"""Contain the class CryptoUtils for getting the current crypto market rate
and the function get_api_key to get the API Key from the local folder file"""
import requests


class CryptoUtils:
    """
    Symbols could get from Binance https://www.binance.com/en/markets/overview
    the requested symbol should be in the High letter case
    example symbols: BTC, ETH, BNB
    """
    def __init__(self, symbol):
        self.price_url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT'

    def get_price(self):
        """Method return the current crypto price from market"""
        data = requests.get(self.price_url)
        data = data.json()
        return data.get('price', 0.0)


def get_api_key():
    """Method gets the API key from local folder file"""
    with open('mm_api_key', 'r') as api_key_file:
        api_key = api_key_file.read()
    return api_key
