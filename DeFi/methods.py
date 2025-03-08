from dataclasses import dataclass


@dataclass
class WebThreeMethods:
    get_balance: str = 'eth_getBalance'
    gas_price: str = 'eth_gasPrice'
    send_transaction: str = 'eth_sendTransaction'
    esimate_gas: str = 'eth_estimateGas'
    get_transaction_count: str = 'eth_getTransactionCount'
    chan_id: str = 'eth_chainId'
    max_priority_fee_per_gas: str = 'eth_maxPriorityFeePerGas'
    accounts: str = 'eth_accounts'
    listen: str = 'net_listening'


@dataclass
class MethodBlocks:
    latest: str = 'latest'
    earliest: str = 'earliest'
    pending: str = 'pending'
    safe: str = 'safe'
    finalized: str = 'finalized'
