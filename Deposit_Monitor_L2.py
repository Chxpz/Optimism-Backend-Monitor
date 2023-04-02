from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json


def monitor_deposits_L2():
    load_dotenv()
    rpc_provider_URL = os.getenv('L2_RPC_PROVIDER_URL')
    private_key = os.getenv('PRIVATE_KEY')
    mongo_string = os.getenv('MONGO_STRING')

    client = MongoClient(mongo_string)
    db = client["OptimismLogs"]
    collection = db["DepositsL2"]


    abi_path_1 = os.path.abspath('./Abis/OVM_L2StandardBridge.json')
    abi_path_2 = os.path.abspath('./Abis/OVM_ETH.json')

    with open(abi_path_1) as f:
        Contract1Abi = json.load(f)

    with open(abi_path_2) as f:
        Contract2Abi = json.load(f)

    CONTRACT_ADDRESS_1 = "0x4200000000000000000000000000000000000010"
    CONTRACT_ADDRESS_2 = "0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000"
    checksum_address = Web3.to_checksum_address(CONTRACT_ADDRESS_2)

    w3 = Web3(Web3.HTTPProvider(rpc_provider_URL))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

    account = Account.from_key(private_key)

    contract1 = w3.eth.contract(address=CONTRACT_ADDRESS_1, abi=Contract1Abi)
    contract2 = w3.eth.contract(address=checksum_address, abi=Contract2Abi)

    event_filter_Transfer = contract2.events.Transfer.create_filter(fromBlock='latest')
    event_filter_Mint = contract2.events.Mint.create_filter(fromBlock='latest')
    event_filter_DepositFinalized = contract1.events.DepositFinalized.create_filter(fromBlock='latest')

    print("Listening for events in L2...")

    while True:
        for event in event_filter_Transfer.get_new_entries():
            event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data'}
            collection.insert_one({
                "contract_address": event['address'],
                "event_name": "Transfer",
                "event_args": event_args,
                "transaction_hash": event['transactionHash'].hex(),
                "timestamp": w3.eth.get_block(event['blockNumber'])['timestamp']
            })

        for event in event_filter_Mint.get_new_entries():
            event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data' and k != 'message'}
            collection.insert_one({
                "contract_address": event['address'],
                "event_name": "Mint",
                "event_args": event_args,
                "transaction_hash": event['transactionHash'].hex(),
                "timestamp": w3.eth.get_block(event['blockNumber'])['timestamp']
            })

        for event in event_filter_DepositFinalized.get_new_entries():
            event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data'}
            collection.insert_one({
                "contract_address": event['address'],
                "event_name": "DepositFinalized",
                "event_args": event_args,
                "transaction_hash": event['transactionHash'].hex(),
                "timestamp": w3.eth.get_block(event['blockNumber'])['timestamp']
            })
            print("New Event added to L2 database")


# Events                # Contract                          # Contract Address          
# Transfer              OVM_ETH                             0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000
# Mint                  OVM_ETH                             0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000

# DepositFinalized      OVM_L2StandardBridge                0x4200000000000000000000000000000000000010

# NoName                OVM_L2CrossDomainMessenger          0x4200000000000000000000000000000000000007
