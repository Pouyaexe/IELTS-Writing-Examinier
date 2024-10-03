from cryptography.fernet import Fernet
import json

# Generate an encryption key (run this only once to generate a key)
key = Fernet.generate_key()
print(f"Encryption Key: {key.decode()}")  # Print the key (you will need to store it in secrets.toml)

# Save the encryption key securely (for reference)
with open("encryption_key.txt", "wb") as key_file:
    key_file.write(key)

# Paths to your JSON files
files_to_encrypt = [
    "tasks/Academic_IELTS_Writing_Task_1_Band_Descriptors.json",
    "tasks/General_Training_IELTS_Writing_Task_1_Band_Descriptors.json",
    "tasks/IELTS_Writing_Task_2_Band_Descriptors.json",
]

# Encrypt each JSON file
cipher = Fernet(key)
for file_path in files_to_encrypt:
    with open(file_path, "r") as f:
        data = f.read()

    # Encrypt the file contents
    encrypted_data = cipher.encrypt(data.encode())

    # Save the encrypted contents
    with open(file_path + ".enc", "wb") as f:
        f.write(encrypted_data)

print("Encryption complete! Encrypted files saved with .enc extension.")
