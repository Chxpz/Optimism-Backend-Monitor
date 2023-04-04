from ETH_Checker import eth_checker
from ERC20_Checker import calculate_differences
from Get_L1_Balances_v2 import Get_L1_Balances_v2
from Balance_Checker_ERC20_L2 import Balance_Checker_ERC20_L2
from Get_Token_Pairs import Get_Token_Pairs
import art

def main():
    while True:
        choice = input("Do you want to analyze Eth Balance or ERC20 Balances? Type 'eth' or 'erc20': ")
        if choice.lower() == 'eth':
            eth_checker()
        elif choice.lower() == 'erc20':
            print("Ok... Let's analyze ERC20 balances...")
            print("Fetching updated data...")
            token_pairs = Get_Token_Pairs()
            ERC20L1_balances = Get_L1_Balances_v2(token_pairs)
            ERC20L2_balances = Balance_Checker_ERC20_L2(token_pairs)
            token_address = input("Input a token address to analyze: ")
            calculate_differences(ERC20L1_balances, ERC20L2_balances, token_address)
        else:
            print("Invalid choice. Please try again.")
            continue

        choice = input("Do you want to continue the analysis? Type 'y' or 'n': ")
        if choice.lower() != 'y':
            break

if __name__ == '__main__':
    try:
        print(art.text2art("Optimism Bridge Monitor"))
        main()
    except Exception as e:
        print(f"Error: {e}")