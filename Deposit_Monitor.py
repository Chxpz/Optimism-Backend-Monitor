from Deposit_Monitor_L1 import monitor_deposits_L1
from Deposit_Monitor_L2 import monitor_deposits_L2
from Get_OVM_ETH_Total_Supply import OVM_ETH_Total_Supply
import threading


def main():
    threads = [threading.Thread(target=monitor_deposits_L1),
               threading.Thread(target=monitor_deposits_L2),
               threading.Thread(target=OVM_ETH_Total_Supply)]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")