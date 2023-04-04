from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.utils.address import to_checksum_address
from dotenv import load_dotenv
from Get_Token_Pairs import Get_Token_Pairs
import os
import json
import time

def Get_L1_Balances_v2(tokenPairs):
    load_dotenv()
    rpc_provider_URL = os.getenv('L1_RPC_PROVIDER_URL')

    abi_path_1 = os.path.abspath('./Abis/L1Monitor.json')

    with open(abi_path_1) as f:
        Contract1Abi = json.load(f)

    L1_MONITOR_ADDR = Web3.to_checksum_address("0x370d6ec27E153E7c225ea2124915f5fDBA5377E0")
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_provider_URL))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    except Exception as e:
        print(f"Error connecting to web3 provider: {e}")

    bridgeAddress = Web3.to_checksum_address("0x99C9fc46f92E8a1c0deC1b1747d010903E884bE1")

    tokenPairs = [(to_checksum_address(pair["tokenL1"]), to_checksum_address(pair["tokenL2"]), pair["balance"]) for pair in tokenPairs]

    L1_Monitor = w3.eth.contract(address=L1_MONITOR_ADDR, abi=Contract1Abi)

    l1_list = []

    
    try:
        balance = L1_Monitor.functions.getBridgebalances(bridgeAddress, tokenPairs).call()
    except Exception as e:
        print(f"Error getting L1 balances: {e}")

    L1_Balances = {"ethBalance": str(balance[1]), "timeStamp": balance[2], "tokenPair": []}
    for i in range(len(balance[0])):
        token = balance[0][i]
        L1_Balances["tokenPair"].append({"tokenL1": token[0], "tokenL2": token[1], "balance": token[2]})
    timestamp = w3.eth.get_block('latest')['timestamp']
    tokenPairsList = [{"tokenL1": str(L1_Balances["tokenPair"][i]["tokenL1"]), "tokenL2": str(L1_Balances["tokenPair"][i]["tokenL2"]), "balance": str(L1_Balances["tokenPair"][i]["balance"])} for i in range(len(tokenPairs))]
    try:
        l1_list.append({
            "tokenPairs": tokenPairsList,
            "ethBalance": str(L1_Balances["ethBalance"]),
            "timeStamp": str(timestamp)
        })
    except Exception as e:
        print(f"Error inserting L1 balances into database: {e}")
    return l1_list

if __name__ == '__main__':
    try:
        tokenPairs = Get_Token_Pairs()
        Get_L1_Balances_v2(tokenPairs)
    except Exception as e:
        print(f"Error: {e}")

