# Metamask Wallet Library

Easy to use with your Metamask address. Also you need to create 
the Metamask developper API_KEY - the instructions how to do 
this you could find on the WEB3 developper portal (also needs 
login credentials):

https://developer.metamask.io/

## 1. Quick Start

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

## API documentation
https://docs.metamask.io/services/reference/bnb-smart-chain/json-rpc-methods/eth_estimategas/
