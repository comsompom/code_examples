# Metamask Wallet Library

## Table of Contents

 1. [Quick Start](#quick-start)
 2. [Library Description](#library-description)
 3. [API documentation](#api-documentation)

Easy to use with your Metamask address. Also you need to create 
the Metamask developper API_KEY - the instructions how to do 
this you could find on the WEB3 developper portal (also needs 
login credentials):

[Developer Portal](https://developer.metamask.io/)


## Quick Start

The quick start code:

```python
from operations import MetamaskOperation


address = "0x107119102c2EC84099cDce3D5eFDE2dcbf4DEB2a"
mm_wallet = MetamaskOperation(address)
# return wallet balance
print(f"Wallet: {address}, balance is: {mm_wallet.get_balance()}")

# return current gas for transaction
print(f"Current gas fee for transaction: {mm_wallet.get_gas_price()}")

# return wallet transaction count
print(f"Wallet: {address}, number transactions: {mm_wallet.get_transaction_count()}")

# return chain id
print(f"Chain ID: {mm_wallet.chain_id()}")

# Returns an estimate of how much priority fee, in wei, you need to be included in a block.
print(f"estimate of how much priority fee: {mm_wallet.max_priority_fee_per_gas()}")
```


## Library Description

The library could connect to different networks that Metamask allowed. The networks 
described in the **networks.py** in the **CryptoNetwork** and could redefine in the 
**MetamaskOperation** class parameter **net_url**

```python
from operations import MetamaskOperation
from networks import CryptoNetwork


address = "0x107119102c2EC84099cDce3D5eFDE2dcbf4DEB2a"
mm_wallet = MetamaskOperation(address)
# redefine the network to Etherium
mm_wallet.net_url = CryptoNetwork().ETHERIUM
# return wallet balance
print(f"Wallet: {address}, balance is: {mm_wallet.get_balance()}")
```


Some Methods of the **MetamaskOperation** are using the **block** parameter in the 
payload. This **block** parameter could be redefine using the **MethodBlocks** class 
from the **operations.py** file

```python
from operations import MetamaskOperation
from methods import MethodBlocks


address = "0x107119102c2EC84099cDce3D5eFDE2dcbf4DEB2a"
mm_wallet = MetamaskOperation(address)
mm_wallet.block = MethodBlocks().earliest
# return wallet balance
print(f"Wallet: {address}, balance is: {mm_wallet.get_balance()}")
```

The **utils.py** fail contain the class **CryptoUtils** which could be used separately 
and independent of the main Metamask library as the class which return the current 
crypto rate from the market. The Symbols name should be in the **CryptoUtils** 
initialisation. The symbol nameshould be in the capital letters. The right symbol 
names could be checked on the Binance online market platform. The return of the 
current crypto symbol in the USDT value.

```python
from utils import CryptoUtils


# get the current BTCUSDT rate from the market
btc_price = CryptoUtils("BTC").get_price()
```


## API documentation
The main documetation based on which was created the library are here:
[Metamask API](https://docs.metamask.io/services/reference/bnb-smart-chain/json-rpc-methods/eth_estimategas/)
