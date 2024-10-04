from Cryptodome.Cipher import AES
import hashlib
import struct

# Helper functions
def get_string(data, offset, length):
    return data[offset:offset+length].decode('utf-8')

def set_big_uint64(buffer, offset, value):
    # Convert the BigInt to 8 bytes (big-endian) and set at offset
    buffer[offset:offset+8] = struct.pack('>Q', value)

def calculate_md5_checksum(iv, encrypted_data):
    md5_hash = hashlib.md5()
    md5_hash.update(iv + encrypted_data)
    return md5_hash.digest()

# Load the card file
with open('testcard.agpay', 'rb') as f:
    card_data = f.read()

# Extract fields from the card
signature = get_string(card_data, 0, 5)
version = get_string(card_data, 5, 2)
encryption_key = card_data[7:39]
reserved = card_data[39:49]
iv = card_data[49:65]
encrypted_data = card_data[65:-22]  # Up to checksum and footer
footer_signature = get_string(card_data, -22, 6)
checksum = card_data[-16:]



# Decrypt the data using AES-CBC
cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
decrypted_data = cipher.decrypt(encrypted_data)

# Convert decrypted_data to bytearray for mutability
decrypted_data = bytearray(decrypted_data)

# Extract balance (8 bytes starting at offset 24)
balance = struct.unpack('>Q', decrypted_data[24:32])[0]
print(f"Original Balance: {balance}")

# Modify the balance
new_balance = 313371337  # Your new balance value here
set_big_uint64(decrypted_data, 24, new_balance)
print(f"Modified Balance: {new_balance}")

# Re-encrypt the modified data
cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
re_encrypted_data = cipher.encrypt(decrypted_data)

# Recalculate the checksum
new_checksum = calculate_md5_checksum(iv, re_encrypted_data)

# Reassemble the card file
new_card_data = card_data[:65] + re_encrypted_data + card_data[-22:-16] + new_checksum

# Save the modified card
with open('modified_card.agpay', 'wb') as f:
    f.write(new_card_data)

# print("Card modification complete. Checking: ")


# print(encrypted_data)
# print(re_encrypted_data)

# print(footer_signature)
# print(card_data[-22:-16])

# print(checksum)
# print(new_checksum)

# print("card data")

# # Print out the combined first version
# print(card_data)


# # Print out the combined second version
# print(card_data[:65] + re_encrypted_data + card_data[-22:-16] + new_checksum)
# print(new_card_data)

