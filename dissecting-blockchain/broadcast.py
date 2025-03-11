import requests
import json
import time
import hashlib

# List of peer nodes
PEERS = ["http://127.0.0.1:5000", "http://127.0.0.1:5001", "http://127.0.0.1:5002"]

# Block structure
class Block:
    def __init__(self, index, previous_hash, data, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Create the blockchain
blockchain = [Block(0, "0", "Genesis Block")]
blockchain.append(Block(1, blockchain[-1].hash, "Blockchain"))
blockchain.append(Block(2, blockchain[-1].hash, "Is"))
blockchain.append(Block(3, blockchain[-1].hash, "Awesome"))

# Convert blockchain to JSON
blockchain_json = json.dumps([block.__dict__ for block in blockchain])

# Broadcast blockchain to peers
for peer in PEERS:
    try:
        response = requests.post(f"{peer}/receive_chain", json={"chain": blockchain_json})
        print(f"Sent to {peer}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send to {peer}: {e}")
