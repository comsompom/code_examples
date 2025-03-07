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
        data = requests.get(self.price_url)
        data = data.json()
        return data['price']
