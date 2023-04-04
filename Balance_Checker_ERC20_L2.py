from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.utils.address import to_checksum_address
from dotenv import load_dotenv
from Get_Token_Pairs import Get_Token_Pairs
import os
import json

def Balance_Checker_ERC20_L2(token_pairs):
    load_dotenv()
    l2_rpc_provider_URL = os.getenv('L2_RPC_PROVIDER_URL')

    abi_path = os.path.abspath('./Abis/ERC20Abi.json')

    with open(abi_path) as f:
        ERC20Abi = json.load(f)
    
    try:
        w3 = Web3(Web3.HTTPProvider(l2_rpc_provider_URL))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    except Exception as e:
        print(f"Error connecting to web3 provider: {e}")
    

    Balance_List = []
    for token_pair in token_pairs:
        L2_ERC20 = w3.eth.contract(address=to_checksum_address(token_pair['tokenL2']), abi=ERC20Abi)
        L2_ERC20_Total_Supply = L2_ERC20.functions.totalSupply().call()
        Balance_List.append({
            "L2_Token": L2_ERC20.address,
            "TotalSupply": L2_ERC20_Total_Supply
        })
        
    
    return Balance_List 


if __name__ == '__main__':
    try:
        token_pairs = Get_Token_Pairs()
        Balance_Checker_ERC20_L2(token_pairs)
    except Exception as e:
        print(f"Error: {e}")
