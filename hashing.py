import hashlib

# Input string
text = "CEN-429 Blockchain for Fintech"

# Compute SHA-256 hash
hash_value = hashlib.sha256(text.encode()).hexdigest()

print("SHA-256 Hash:", hash_value)

modified_text = 'COMP1830-Blockchain for Fintech'
modified_hash_value = hashlib.sha256(modified_text.encode()).hexdigest()
print('--------------------------------------------------------------------------------------------')
print("Modified SHA-256 Hash: ", modified_hash_value)