API_KEY = 'DH6J71U6BRQWFG5PMPG37PQ76IB9WFDU26'

import json
import requests

weis_address = '0xEeC84548aAd50A465963bB501e39160c58366692'

API_REQUEST = "https://api.etherscan.io/v2/api?chainid=1&module=account&action=balancemulti&address=" + weis_address + "&tag=latest&apikey=" + API_KEY
resp = requests.get(API_REQUEST)

# Parse JSON string into Python dictionary
data = json.loads(resp.text)

balance_weis = data['result'][0]['balance']
print(f'Balance of Weis account is: {balance_weis}')
print(f"Balance in ETH: {float(balance_weis) / 1e18} ETH")  # Convert Weis to ETH
