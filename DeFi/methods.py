from dataclasses import dataclass


@dataclass
class EtheriumMethods:
    get_balance: str = 'eth_getBalance'
    gas_price: str = 'eth_gasPrice'
    send_transaction: str = 'eth_sendTransaction'
    esimate_gas: str = 'eth_estimateGas'
