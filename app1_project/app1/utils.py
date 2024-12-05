from decouple import config
from cryptography.fernet import Fernet

# Load the secret key from the .env file
SECRET_KEY = config("FERNET_SECRET_KEY")

# Initialize the cipher using the loaded key
cipher = Fernet(SECRET_KEY.encode())

def encrypt_message(plain_text):
    return cipher.encrypt(plain_text.encode()).decode()

from cryptography.fernet import Fernet

# Generate a new key
key = Fernet.generate_key()

# Print the key in a readable format
print(key.decode())  # decode the key to a string for storage
