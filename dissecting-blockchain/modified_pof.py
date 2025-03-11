import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, data, difficulty, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.difficulty = difficulty  # Number of leading zeros required
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.compute_proof_of_work()

    def compute_proof_of_work(self):
        while True:
            block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{self.nonce}"
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()
            if block_hash.startswith("0" * self.difficulty):
                return block_hash
            self.nonce += 1

# Test with different difficulty levels
for difficulty in [2, 4, 6]:  # Modify the prefix length
    start_time = time.time()
    block = Block(1, "0", "Test Block", difficulty)
    end_time = time.time()
    print(f"Difficulty: {difficulty}, Hash: {block.hash}, Time Taken: {end_time - start_time:.4f} seconds")
