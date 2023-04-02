from web3 import Web3
from eth_account import Account
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json


load_dotenv()
rpc_provider_URL = os.getenv('RPC_PROVIDER_URL')
private_key = os.getenv('PRIVATE_KEY')
mongo_string = os.getenv('MONGO_STRING')

client = MongoClient(mongo_string)
db = client["OptimismLogs"]
collection = db["Deposits"]

abi_path_1 = os.path.abspath('./Abis/CanonicalTransactionChain.json')
abi_path_2 = os.path.abspath('./Abis/Lib_ResolveDelegateProxy.json')
abi_path_3 = os.path.abspath('./Abis/L1ChugSplashProxy.json')

with open(abi_path_1) as f:
    Contract1Abi = json.load(f)

with open(abi_path_2) as f:
    Contract2Abi = json.load(f)

with open(abi_path_3) as f:
    Contract3Abi = json.load(f)

CONTRACT_ADDRESS_1 = "0x5E4e65926BA27467555EB562121fac00D24E9dD2"
CONTRACT_ADDRESS_2 = "0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1"
CONTRACT_ADDRESS_3 = "0x99C9fc46f92E8a1c0deC1b1747d010903E884bE1"



w3 = Web3(Web3.HTTPProvider(rpc_provider_URL))
# w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

account = Account.from_key(private_key)

contract1 = w3.eth.contract(address=CONTRACT_ADDRESS_1, abi=Contract1Abi)
contract2 = w3.eth.contract(address=CONTRACT_ADDRESS_2, abi=Contract2Abi)
contract3 = w3.eth.contract(address=CONTRACT_ADDRESS_3, abi=Contract3Abi)

event_filter_1 = contract1.events.TransactionEnqueued.create_filter(fromBlock='latest')
event_filter_2 = contract2.events.SentMessage.create_filter(fromBlock='latest')
event_filter_3 = contract3.events.ETHDepositInitiated.create_filter(fromBlock='latest')

print("Listening for events...")

while True:
    for event in event_filter_1.get_new_entries():
        event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data'}
        collection.insert_one({
            "contract_address": event['address'],
            "event_name": "TransactionEnqueued",
            "event_args": event_args
        })
        
    for event in event_filter_2.get_new_entries():
        event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data' and k != 'message'}
        collection.insert_one({
            "contract_address": event['address'],
            "event_name": "SentMessage",
            "event_args": event_args
        })

    for event in event_filter_3.get_new_entries():
        event_args = {k: v.decode('latin-1') if isinstance(v, bytes) else v for k, v in event['args'].items() if k != '_data'}
        collection.insert_one({
            "contract_address": event['address'],
            "event_name": "ETHDepositInitiated",
            "event_args": event_args
        })
        print("New Event added to database")