from web3 import Web3
from web3.middleware import geth_poa_middleware
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import time

def OVM_ETH_Total_Supply():
    load_dotenv()
    rpc_provider_URL = os.getenv('L2_RPC_PROVIDER_URL')
    mongo_string = os.getenv('MONGO_STRING')

    client = MongoClient(mongo_string)
    db = client["OptimismLogs"]
    collection = db["OVM_ETH_Total_Supply"]

    abi_path_1 = os.path.abspath('./Abis/OVM_ETH.json')

    with open(abi_path_1) as f:
        Contract1Abi = json.load(f)

    OVM_ETH_CONTRACT_ADDRESS = "0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000"
    OVM_ETH_CONTRACT_ADDRESS_CHECKSUM = Web3.to_checksum_address(OVM_ETH_CONTRACT_ADDRESS)

    w3 = Web3(Web3.HTTPProvider(rpc_provider_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    OVM_ETH = w3.eth.contract(address=OVM_ETH_CONTRACT_ADDRESS_CHECKSUM, abi=Contract1Abi)

    while True:
        total_supply = str(OVM_ETH.functions.totalSupply().call())
        timestamp = w3.eth.get_block('latest')['timestamp']
        collection.insert_one({
            "OP-ETH-Supply": total_supply,
            "timestamp": timestamp
        })
        time.sleep(180)
        print("OP-ETH-Supply: ", total_supply, "Timestamp: ", timestamp)

if __name__ == '__main__':
    try:
        OVM_ETH_Total_Supply()
    except Exception as e:
        print(f"Error: {e}")