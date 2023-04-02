import os
import json

def Get_Token_Pairs():
    # get the path of the json file
    json_path = os.path.join(os.getcwd(), "utils", "OP_TokenList.json")

    # load the json data
    with open(json_path, 'r') as f:
        data = json.load(f)

    # get the list of token names to filter
    token_names = [token["name"] for token in data["tokens"] if token["chainId"] == 1]

    # create the tokenPairs list
    tokenPairs = []
    for token in data["tokens"]:
        if token["name"] in token_names and token["chainId"] == 10:
            tokenPairs.append({
                "tokenL1": [token2["address"] for token2 in data["tokens"] if token2["name"] == token["name"] and token2["chainId"] == 1][0],
                "tokenL2": token["address"],
                "balance": 0
            })

    # return the tokenPairs list
    return tokenPairs

if __name__ == '__main__':
    try:
        Get_Token_Pairs()
    except Exception as e:
        print(f"Error: {e}")

