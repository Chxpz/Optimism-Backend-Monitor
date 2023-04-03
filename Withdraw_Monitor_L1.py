from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

def monitor_withdraw_L1():
    load_dotenv()
    rpc_provider_URL = os.getenv('L1_RPC_PROVIDER_URL')
    private_key = os.getenv('PRIVATE_KEY')
    mongo_string = os.getenv('MONGO_STRING')

    client = MongoClient(mongo_string)
    db = client["OptimismLogs"]
    collection = db["WithdrawL1"]

    abi_path_1 = os.path.abspath('./Abis/L1ChugSplashProxy.json')

    with open(abi_path_1) as f:
        Contract1Abi = json.load(f)

    CONTRACT_ADDRESS_1 = "0x99C9fc46f92E8a1c0deC1b1747d010903E884bE1"


    try:
        w3 = Web3(Web3.HTTPProvider(rpc_provider_URL))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    except Exception as e:
        print(f"Error connecting to web3 provider: {e}")

    account = Account.from_key(private_key)

    contract1 = w3.eth.contract(address=CONTRACT_ADDRESS_1, abi=Contract1Abi)

    event_ETHWithdrawal = contract1.events.ETHWithdrawalFinalized.create_filter(fromBlock='latest')
    event_ERC20Withdrawal = contract1.events.ERC20WithdrawalFinalized.create_filter(fromBlock='latest')

    print("Listening for withdraw events in L1...")

    while True:
        for event in event_ETHWithdrawal.get_new_entries():
            tx_hash = event['transactionHash'].hex()
            block_number = event['blockNumber']
            block_timestamp = w3.eth.get_block(block_number).timestamp
            event_args = {
                k: v.decode('latin-1') if isinstance(v, bytes) else v
                for k, v in event['args'].items()
                if k != '_data'
            }
            try:
                collection.insert_one({
                    "contract_address": event['address'],
                    "event_name": "ETHWithdrawalFinalized",
                    "from": str(event_args['_from']),
                    "to": str(event_args['_to']),
                    "amount": str(event_args['_amount']),
                    "tx_hash": tx_hash,
                    "timestamp": block_timestamp
                })
            except Exception as e:
                print(f"Error inserting L1 withdraw event into database: {e}")
        
        for event in event_ERC20Withdrawal.get_new_entries():
            tx_hash = event['transactionHash'].hex()
            block_number = event['blockNumber']
            block_timestamp = w3.eth.get_block(block_number).timestamp
            event_args = {
                k: v.decode('latin-1') if isinstance(v, bytes) else v
                for k, v in event['args'].items()
                if k != '_data'
            }
            try:
                collection.insert_one({
                    "contract_address": event['address'],
                    "event_name": "ERC20WithdrawalFinalized",
                    "l1Token": str(event_args['_l1Token']),
                    "l2Token": str(event_args['_l2Token']),
                    "from": str(event_args['_from']),
                    "to": str(event_args['_to']),
                    "amount": str(event_args['_amount']),
                    "tx_hash": tx_hash,
                    "timestamp": block_timestamp
                })
            except Exception as e:
                print(f"Error inserting L1 withdraw event into database: {e}")
            
            print("New Withdraw Event added to L1 database")