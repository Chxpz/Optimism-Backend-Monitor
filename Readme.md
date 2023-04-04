# Optimism Bridge Monitor
This Python script allows you to monitor the balances of Ethereum and ERC20 tokens on the Ethereum and Optimism Layer 2 network.

>Note: Considering the bridge between the two layers there is an expectation that the balances on L1 are reflected on L2. Any huge discrepancy should be treated as a potential Risk and the indication of potential exploit on the Bridge.

>The ETH analysis does not provide any assessment on Risk, it is up to the user to determine if a Risk exists or not, what the script does is presenting the data necessary to the user to assess and determine by its own if a risk exists or not.

>The ERC20 does present a risk assessment benchmark
> - Differences up to 10% will be shown as low
> - Differences from 10% to 15 will be shown as medium
> - Differences higher than 15% will be shown as high
> This is only to have present a parameter to the user, however if the user judges 5% as a high risk, that is fine., you are able to see this difference using this script and move your money if needed. 

> ### It is important to consider that each deposit from L1 to L2 has a delay of ~20 minutes and each withdraw from L2 to L1 has a delay of ~7 days, this has an impact when comparing the balances in both layers and should be taken into consideration.

## Getting started
To use the script, you'll need to set up a Python virtual environment and install the necessary packages. Here are the steps to do that:

* Clone this repository to your local machine.

* Navigate to the root directory of the repository in your terminal.

* Run python3 -m venv venv to create a new Python virtual environment called 'venv'.

* Activate the virtual environment by running source venv/bin/activate on macOS/Linux or .\venv\Scripts\activate on Windows.

* Install the required packages by running pip install -r requirements.txt.

* Create a .env file in the root directory of the repository with the following contents:

## Set-up provider connection

In your .env file set up the provider connection for L1 and L2.

```bash
L1_RPC_PROVIDER_URL=<Add your provider URL>
```
```bash
L2_RPC_PROVIDER_URL=<Add your provider URL>
```
## Usage
To use the script, simply run:
 ```bash
    python3 MonitorUp.py
```
You'll be prompted to choose whether you want to analyze ETH balances or ERC20 balances.

## Analyzing ETH balances
If you choose to analyze ETH balances, the script will retrieve the ETH balance on both the Ethereum network and the Optimism network, and calculate the difference between them. You'll be shown a table with the following columns:

* Balance: The name of the network.
* L1: The ETH balance on the Ethereum network.
* L2: The ETH balance on the Optimism network.
* Difference: The difference between the two balances.
* % Difference: The percentage difference between the two balances.

## Analyzing ERC20 balances
If you choose to analyze ERC20 balances, the script will retrieve the balances of all ERC20 tokens on both the Ethereum network and the Optimism network, and calculate the difference between them for a specific token that you choose. You'll be prompted to enter the address of the token you want to analyze.

You'll be shown a table with the following columns:

* L1 Token: The name of the token on the Ethereum network.
* L2 Token: The name of the token on the Optimism network.
* Difference: The difference between the two balances.
* % Difference: The percentage difference between the two balances.
* Risk: A risk rating based on the percentage difference.

## Acknowledgements
This project uses the following open-source packages:

* Web3.py
* python-dotenv
* art