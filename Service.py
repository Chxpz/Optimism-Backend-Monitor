from pymongo import MongoClient
from decimal import Decimal
from dotenv import load_dotenv
import os

def process_monitor():

    load_dotenv()
    mongo_string = os.getenv('MONGO_STRING')

    client = MongoClient(mongo_string)

    db = client["OptimismLogs"]
    Eth_Balance_Difference = db["eth-balance-difference"]

    DepositsL1 = db["DepositsL1"]
    DepositsL2 = db["DepositsL2"]
    OVM_ETH_Total_Supply = db["OVM_ETH_Total_Supply"]
    WithdrawL1 = db["WithdrawL1"]
    WithdrawL2 = db["WithdrawL2"]
    L1_Balances = db["L1_Balances"]

    total_supply_cursor = OVM_ETH_Total_Supply.find().sort("timestamp", 1)
    total_eth_balance_cursor = L1_Balances.find().sort("timeStamp", 1)

    total_supply = Decimal('0')
    total_eth_balance = Decimal('0')
    total_supply_timestamp = None
    total_eth_balance_timestamp = None

    for supply_doc in total_supply_cursor:
        if total_supply_timestamp != supply_doc["timestamp"]:
            # New timestamp, calculate difference and save to new collection
            if total_supply_timestamp is not None and total_eth_balance_timestamp is not None:
                difference = total_supply - total_eth_balance
                Eth_Balance_Difference.insert_one({
                    "timestamp": total_supply_timestamp,
                    "difference": str(difference)
                })

            # Reset values for new timestamp
            total_supply = Decimal(str(supply_doc["OP-ETH-Supply"]))
            total_supply_timestamp = supply_doc["timestamp"]

        else:
            # Same timestamp, accumulate total supply
            total_supply += Decimal(str(supply_doc["OP-ETH-Supply"]))

        # Find the corresponding total_eth_balance document
        while total_eth_balance_timestamp is None or total_eth_balance_timestamp < supply_doc["timestamp"]:
            eth_balance_doc = total_eth_balance_cursor.next()
            total_eth_balance = Decimal(str(eth_balance_doc["ethBalance"]))
            total_eth_balance_timestamp = eth_balance_doc["timeStamp"]

        if total_supply_timestamp == total_eth_balance_timestamp:
            # Found corresponding eth_balance document, calculate difference and save to new collection
            difference = total_supply - total_eth_balance
            Eth_Balance_Difference.insert_one({
                "timestamp": total_supply_timestamp,
                "difference": str(difference)
            })


if __name__ == '__main__':
    try:
        process_monitor()
    except Exception as e:
        print(f"Error: {e}")