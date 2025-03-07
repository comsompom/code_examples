from dataclasses import dataclass


@dataclass
class EtheriumMethods:
    get_balance: str = 'eth_getBalance'
    gas_price: str = 'eth_gasPrice'
    send_transaction: str = 'eth_sendTransaction'
    esimate_gas: str = 'eth_estimateGas'
    get_transaction_count: str = 'eth_getTransactionCount'
    chan_id: str = 'eth_chainId'
    max_priority_fee_per_gas: str = 'eth_maxPriorityFeePerGas'
