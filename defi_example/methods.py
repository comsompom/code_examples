# pylint: disable=E0401
# pylint: disable=R0902
"""
Dataclasses for:
 WebThreeMethods which describe the methods fo the Metamask
 and MethodBlocks for describe the blocks of the parameters
"""

from dataclasses import dataclass


@dataclass
class WebThreeMethods:
    """Dataclass for describe the possible metamask methods"""
    get_balance: str = 'eth_getBalance'
    gas_price: str = 'eth_gasPrice'
    send_transaction: str = 'eth_sendTransaction'
    esimate_gas: str = 'eth_estimateGas'
    get_transaction_count: str = 'eth_getTransactionCount'
    chan_id: str = 'eth_chainId'
    max_priority_fee_per_gas: str = 'eth_maxPriorityFeePerGas'
    accounts: str = 'eth_accounts'
    listen: str = 'net_listening'
    peer_nums: str = 'net_peerCount'


@dataclass
class MethodBlocks:
    """Dataclass for describing the blocks of the parameters"""
    latest: str = 'latest'
    earliest: str = 'earliest'
    pending: str = 'pending'
    safe: str = 'safe'
    finalized: str = 'finalized'
