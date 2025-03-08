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

# Returns a list of addresses owned by the client.
print(f"User accounts number: {mm_wallet.accounts()}")

# Returns true if client is actively listening for network connections.
print(f"Client all time listening the network: {mm_wallet.listening()}")

# Returns the number of peers currently connected to the client.
print(f"Number of the peers connected to the client: {mm_wallet.peer_nums()}")