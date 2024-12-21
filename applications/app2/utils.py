from decouple import config
from cryptography.fernet import Fernet

# Load the secret key from the .env file and encode it
SECRET_KEY = config('FERNET_SECRET_KEY').encode()

# Initialize the cipher using the shared key
cipher = Fernet(SECRET_KEY)

def decrypt_message(encrypted_message):
    """Decrypt the encrypted message."""
    return cipher.decrypt(encrypted_message.encode()).decode()
