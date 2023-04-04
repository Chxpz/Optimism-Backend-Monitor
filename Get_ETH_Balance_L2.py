from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import os
import json

def get_eth_l2():
    load_dotenv()
    rpc_provider_URL = os.getenv('L2_RPC_PROVIDER_URL')

    abi_path_1 = os.path.abspath('./Abis/OVM_ETH.json')

    with open(abi_path_1) as f:
        Contract1Abi = json.load(f)

    OVM_ETH_CONTRACT_ADDRESS = "0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000"
    OVM_ETH_CONTRACT_ADDRESS_CHECKSUM = Web3.to_checksum_address(OVM_ETH_CONTRACT_ADDRESS)

    try:
        w3 = Web3(Web3.HTTPProvider(rpc_provider_URL))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    except Exception as e:
        print(f"Error connecting to web3 provider: {e}")

    OVM_ETH = w3.eth.contract(address=OVM_ETH_CONTRACT_ADDRESS_CHECKSUM, abi=Contract1Abi)


    try:
        total_supply = str(OVM_ETH.functions.totalSupply().call())
    except Exception as e:
        print(f"Error: {e}")
    
    return total_supply

if __name__ == '__main__':
    try:
        get_eth_l2()
    except Exception as e:
        print(f"Error: {e}")