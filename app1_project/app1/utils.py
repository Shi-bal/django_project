from decouple import config
from cryptography.fernet import Fernet

# Load the secret key from the .env file
SECRET_KEY = config("FERNET_SECRET_KEY")

# Initialize the cipher using the loaded key
cipher = Fernet(SECRET_KEY.encode())

def encrypt_message(plain_text):
    return cipher.encrypt(plain_text.encode()).decode()
