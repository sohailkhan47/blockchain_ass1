from flask import Flask, request, jsonify
import requests
import json
import time
import hashlib
import sys

app = Flask(__name__)

# Node blockchain
blockchain = []

# List of known peer nodes
PEERS = set()

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

# Create the Genesis Block
def create_genesis_block():
    return Block(0, "0", "Genesis Block")

blockchain.append(create_genesis_block())

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain]
    return jsonify(chain_data), 200

@app.route('/receive_chain', methods=['POST'])
def receive_chain():
    global blockchain
    chain_data = request.json.get("chain")
    if not chain_data:
        return jsonify({"message": "Invalid chain data"}), 400

    # Convert JSON to blockchain format (excluding hash field)
    received_chain = [Block(block["index"], block["previous_hash"], block["data"], block["timestamp"]) for block in json.loads(chain_data)]
    
    # Validate and replace chain if it's longer
    if len(received_chain) > len(blockchain):
        blockchain = received_chain
        return jsonify({"message": "Blockchain updated"}), 200
    return jsonify({"message": "Received chain is not longer"}), 400

@app.route('/add_peer', methods=['POST'])
def add_peer():
    peer = request.json.get("peer")
    if peer:
        PEERS.add(peer)
        return jsonify({"message": "Peer added"}), 200
    return jsonify({"message": "Invalid peer"}), 400

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python peer.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    app.run(host='127.0.0.1', port=port, debug=True)
