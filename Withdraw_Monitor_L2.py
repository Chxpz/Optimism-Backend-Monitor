from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json


def monitor_withdraw_L2():
    load_dotenv()
    rpc_provider_URL = os.getenv('L2_RPC_PROVIDER_URL')
    private_key = os.getenv('PRIVATE_KEY')
    mongo_string = os.getenv('MONGO_STRING')

    client = MongoClient(mongo_string)
    db = client["OptimismLogs"]
    collection = db["WithdrawL2"]


    abi_path_1 = os.path.abspath('./Abis/OVM_L2StandardBridge.json')
    abi_path_2 = os.path.abspath('./Abis/OVM_ETH.json')

    with open(abi_path_1) as f:
        Contract1Abi = json.load(f)

    with open(abi_path_2) as f:
        Contract2Abi = json.load(f)

    CONTRACT_ADDRESS_1 = "0x4200000000000000000000000000000000000010"
    CONTRACT_ADDRESS_2 = "0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000"
    checksum_address = Web3.to_checksum_address(CONTRACT_ADDRESS_2)

    try:
        w3 = Web3(Web3.HTTPProvider(rpc_provider_URL))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    except Exception as e:
        print(f"Error connecting to web3 provider: {e}")

    account = Account.from_key(private_key)

    contract1 = w3.eth.contract(address=CONTRACT_ADDRESS_1, abi=Contract1Abi)
    contract2 = w3.eth.contract(address=checksum_address, abi=Contract2Abi)

    event_filter_Transfer = contract2.events.Transfer.create_filter(fromBlock='latest')
    event_filter_Burn = contract2.events.Burn.create_filter(fromBlock='latest')
    event_filter_WithdrawalInitiated = contract1.events.WithdrawalInitiated.create_filter(fromBlock='latest')

    print("Listening for withdraw events in L2...")

    while True:
        for event in event_filter_Transfer.get_new_entries():
            event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data'}
            try:
                collection.insert_one({
                    "contract_address": event['address'],
                    "event_name": "Transfer",
                    "from": str(event_args['from']),
                    "to": str(event_args['to']),
                    "value": str(event_args['value']),
                    "transaction_hash": event['transactionHash'].hex(),
                    "timestamp": w3.eth.get_block(event['blockNumber'])['timestamp']
                })
            except Exception as e:
                print(f"Error inserting withdraw event into database: {e}")

        for event in event_filter_Burn.get_new_entries():
            event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data' and k != 'message'}
            try:
                collection.insert_one({
                    "contract_address": event['address'],
                    "event_name": "Burn",
                    "account": str(event_args['_account']),
                    "amount": str(event_args['_amount']),
                    "transaction_hash": event['transactionHash'].hex(),
                    "timestamp": w3.eth.get_block(event['blockNumber'])['timestamp']
                })
            except Exception as e:
                print(f"Error inserting withdraw event into database: {e}")

        for event in event_filter_WithdrawalInitiated.get_new_entries():
            event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data'}
            try:
                collection.insert_one({
                    "contract_address": event['address'],
                    "event_name": "WithdrawalInitiated",
                    "l1Token": str(event_args['_l1Token']),
                    "l2Token": str(event_args['_l2Token']),
                    "from": str(event_args['_from']),
                    "to": str(event_args['_to']),
                    "amount": str(event_args['_amount']),
                    "transaction_hash": event['transactionHash'].hex(),
                    "timestamp": w3.eth.get_block(event['blockNumber'])['timestamp']
                })
            except Exception as e:
                print(f"Error inserting withdraw event into database: {e}")
            print("New Withdraw Event added to L2 database")
