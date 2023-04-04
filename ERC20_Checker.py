from Get_L1_Balances_v2 import Get_L1_Balances_v2
from Balance_Checker_ERC20_L2 import Balance_Checker_ERC20_L2
from Get_Token_Pairs import Get_Token_Pairs
import art

def calculate_differences(ERC20L1_balances, ERC20L2_balances, token_address):
    results = []
    for obj1 in ERC20L1_balances:
        for token_pair in obj1['tokenPairs']:
            if token_pair['tokenL1'].lower() == token_address.lower() or token_pair['tokenL2'].lower() == token_address.lower():
                tokenL2 = token_pair['tokenL2']
                balance = int(token_pair['balance'])
                match = next((item for item in ERC20L2_balances if item['L2_Token'] == tokenL2), None)
                if match:
                    total_supply = int(match['TotalSupply'])
                    difference = balance - total_supply
                    average = (balance + total_supply) / 2
                    percentage_difference = abs(difference) / average * 100 if average != 0 else 0
                    risk = 'high' if percentage_difference > 15 else ('medium' if percentage_difference > 10 else 'low')
                    results.append({
                        'TokenL1': token_pair['tokenL1'],
                        'TokenL2': tokenL2,
                        'Difference': difference,
                        'PercentageDifference': percentage_difference,
                        'Risk': risk
                    })
    if len(results) == 0:
        print(f"No results found for token address {token_address}")
    else:
        print("+----------------------------------------------+----------------------------------------------+----------------------+-----------------+-----------+")
        print("| L1 Token                                     | L2 Token                                     | Difference           | % Difference    | Risk      |")
        print("+----------------------------------------------+----------------------------------------------+----------------------+-----------------+-----------+")
        for result in results:
            if result['TokenL1'].lower() == token_address.lower():
                l1_token = result['TokenL1']
                l2_token = result['TokenL2']
                difference = result['Difference']
                percentage_difference = "{:.2f}%".format(abs(result['PercentageDifference']))
                risk = result['Risk']
            elif result['TokenL2'].lower() == token_address.lower():
                l1_token = next(item['TokenL1'] for item in results if item['TokenL2'].lower() == token_address.lower())
                l2_token = result['TokenL2']
                difference = -result['Difference']  # negate the difference for L2 tokens
                percentage_difference = "{:.2f}%".format(abs(result['PercentageDifference']))
                risk = result['Risk']
            difference_formatted = "{:,.2f}".format(difference)
            print("| {:<44} | {:<44} | {:>20} | {:>15} | {:<9} |".format(l1_token, l2_token, difference_formatted, percentage_difference, risk))
        print("+----------------------------------------------+----------------------------------------------+----------------------+-----------------+-----------+")
    return

if __name__ == '__main__':
    try:
        print(art.text2art("Optimism Bridge Monitor"))
        print("Setting up everything...")
        token_pairs = Get_Token_Pairs()
        ERC20L1_balances = Get_L1_Balances_v2(token_pairs)
        ERC20L2_balances = Balance_Checker_ERC20_L2(token_pairs)
        while True:
            token_address = input("Input a token address to analyze: ")
            calculate_differences(ERC20L1_balances, ERC20L2_balances, token_address)
            choice = input("Want to Analyze another token? Y/N ")
            if choice.lower() == 'n':
                break
        print("Thank you")
    except Exception as e:
        print(f"Error: {e}")

