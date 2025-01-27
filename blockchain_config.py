from web3 import Web3
import requests

from settings import settings

web3 = Web3(Web3.HTTPProvider(f"{settings.blockchain_url}:{settings.blockchain_port}"))

if not web3.is_connected():
    raise ConnectionError("Failed to connect to blockchain")


response = requests.get(
    f"{settings.blockchain_url}:{settings.abi_port}/Crowdfunding.sol/Crowdfunding.json"
)

try:
    crowdfunding_abi = response.json()["abi"]
except Exception as e:
    raise ValueError(f"Failed to decode ABI JSON, {e}")
print(crowdfunding_abi)
contract = web3.eth.contract(address=settings.contract_address, abi=crowdfunding_abi)
