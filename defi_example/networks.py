# pylint: disable=C0103
from dataclasses import dataclass


@dataclass
class CryptoNetwork:
    """Dataclas for describing the possible Metamask networks"""
    BNB: str = 'https://bsc-mainnet.infura.io/v3/'
    ARBITRUM: str = 'https://arbitrum-mainnet.infura.io/v3/'
    BASE: str = 'https://base-sepolia.infura.io/v3/'
    BLAST: str = 'https://blast-mainnet.infura.io/v3/'
    CELO: str = 'https://celo-mainnet.infura.io/v3/'
    ETHERIUM: str = 'https://mainnet.infura.io/v3/'
    LINEA: str = 'https://linea-mainnet.infura.io/v3/'
    MANTLE: str = 'https://mantle-mainnet.infura.io/v3/'
    opBNB: str = 'https://opbnb-mainnet.infura.io/v3/'
    POLYGONPOS: str = 'https://polygon-mainnet.infura.io/v3/'
