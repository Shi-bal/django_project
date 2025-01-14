from decouple import config
from cryptography.fernet import Fernet

# Load the secret key from the .env file and encode it
SECRET_KEY = config("FERNET_SECRET_KEY").encode()

# Initialize the cipher using the shared key
cipher = Fernet(SECRET_KEY)

def encrypt_message(message):
    """Encrypt the message using the shared key."""
    return cipher.encrypt(message.encode()).decode()
