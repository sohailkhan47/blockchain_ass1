import json
import requests

address = '1Dorian4RoXcnBv9hnQ4Y2C1an6NJ4UrjX'

resp = requests.get('https://blockchain.info/unspent?active=%s' % address)

utxo_set = json.loads(resp.text)['unspent_outputs']

total_balance = sum(utxo['value'] for utxo in utxo_set)

print(f"Total Balance: {total_balance} Satoshis ({total_balance / 100_000_000} BTC)")
