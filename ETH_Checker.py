from Get_ETH_Balance_L2 import get_eth_l2
from Get_L1_Balances_v2 import Get_L1_Balances_v2

def eth_checker():
    eth_balance_l2 = int(get_eth_l2())
    L1_balances = Get_L1_Balances_v2({})
    eth_balance_l1 = int(L1_balances[0]['ethBalance'])

    eth_balance_l1_formatted = "{:,.2f}".format(eth_balance_l1 / 10**18)
    eth_balance_l2_formatted = "{:,.2f}".format(eth_balance_l2 / 10**18)
    difference = eth_balance_l2 - eth_balance_l1
    difference_formatted = "{:,.2f}".format(difference / 10**18)
    percentage_difference = abs(difference / eth_balance_l1) * 100
    percentage_difference_formatted = "{:.2f}%".format(percentage_difference)

    print("+-----------------+-----------------+-----------------+-----------------+-----------------+")
    print("|     Balance     |       L1        |       L2        |    Difference   | % Difference    |")
    print("+-----------------+-----------------+-----------------+-----------------+-----------------+")
    print("| Eth             | {:>15} | {:>15} | {:>15} | {:>15} |".format(eth_balance_l1_formatted, eth_balance_l2_formatted, difference_formatted, percentage_difference_formatted))
    print("+-----------------+-----------------+-----------------+-----------------+-----------------+")

if __name__ == '__main__':
    try:
        eth_checker()
    except Exception as e:
        print(f"Error: {e}")