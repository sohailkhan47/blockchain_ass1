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

# Create blockchain with 10 blocks
blockchain = [Block(0, "0", "Genesis Block")]

for i in range(1, 10):
    blockchain.append(Block(i, blockchain[-1].hash, f"Block {i}"))

# Perform attack: Modify the second block's data
blockchain[1].data = "Tampered Data"
blockchain[1].hash = blockchain[1].compute_hash()

# Recalculate hashes for all subsequent blocks
for i in range(2, len(blockchain)):
    blockchain[i].previous_hash = blockchain[i - 1].hash
    blockchain[i].hash = blockchain[i].compute_hash()

# Convert blockchain to JSON
blockchain_json = json.dumps([block.__dict__ for block in blockchain])

# Broadcast the modified blockchain
for peer in PEERS:
    try:
        response = requests.post(f"{peer}/receive_chain", json={"chain": blockchain_json})
        print(f"Sent to {peer}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send to {peer}: {e}")
