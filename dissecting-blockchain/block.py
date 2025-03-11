import hashlib
import time

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

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, data)
        self.chain.append(new_block)

    def get_last_block_hash(self):
        return self.chain[-1].hash

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Recalculate the hash of the current block
            if current_block.hash != current_block.compute_hash():
                return False

            # Check if the previous hash stored in the block is correct
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def modify_block(self, index, new_data):
        if 0 < index < len(self.chain):  # Prevent modifying the genesis block
            self.chain[index].data = new_data
            self.chain[index].hash = self.chain[index].compute_hash()
            print(f"Block {index} modified. New hash: {self.chain[index].hash}")

# Step 1: Create the blockchain
blockchain = Blockchain()
blockchain.add_block("Blockchain")
blockchain.add_block("Is")
blockchain.add_block("Awesome")

# Step 2: Get the hash of the last block before modification
print("Original last block hash:", blockchain.get_last_block_hash())

# Step 3: Modify the 3rd block's data ("Is" → "Is very")
blockchain.modify_block(2, "Is very")

# Step 4: Check blockchain validity
if blockchain.is_chain_valid():
    print("Blockchain is still valid.")
else:
    print("Blockchain is INVALID due to modification!")

# Step 5: Correct the blockchain by regenerating all subsequent hashes
for i in range(3, len(blockchain.chain)):  # Update all blocks after modification
    blockchain.chain[i].previous_hash = blockchain.chain[i - 1].hash
    blockchain.chain[i].hash = blockchain.chain[i].compute_hash()

# Step 6: Get the new final hash
print("Corrected last block hash:", blockchain.get_last_block_hash())
