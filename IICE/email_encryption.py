from cryptography.fernet import Fernet
from django.conf import settings
import os
import base64

class EmailPasswordEncryption:
    """
    Utility class for encrypting and decrypting email passwords
    """
    
    @staticmethod
    def generate_key():
        """
        Generate a new encryption key
        """
        return Fernet.generate_key()
    
    @staticmethod
    def get_or_create_key():
        """
        Get existing encryption key from environment or create a new one
        """
        key = os.environ.get('EMAIL_ENCRYPTION_KEY')
        if not key:
            # Generate a new key if none exists
            new_key = Fernet.generate_key()
            print(f"Generated new encryption key: {new_key.decode()}")
            print("Please add this to your .env file as EMAIL_ENCRYPTION_KEY")
            return new_key
        return key.encode() if isinstance(key, str) else key
    
    @staticmethod
    def encrypt_password(password):
        """
        Encrypt the email password
        """
        key = EmailPasswordEncryption.get_or_create_key()
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        return base64.urlsafe_b64encode(encrypted_password).decode()
    
    @staticmethod
    def decrypt_password(encrypted_password):
        """
        Decrypt the email password
        """
        try:
            key = EmailPasswordEncryption.get_or_create_key()
            fernet = Fernet(key)
            decoded_password = base64.urlsafe_b64decode(encrypted_password.encode())
            decrypted_password = fernet.decrypt(decoded_password)
            return decrypted_password.decode()
        except Exception as e:
            print(f"Error decrypting password: {e}")
            # Fallback to plain text if decryption fails (for backward compatibility)
            return encrypted_password
    
    @staticmethod
    def is_encrypted(password):
        """
        Check if a password is already encrypted
        """
        try:
            # Try to decode as base64 - encrypted passwords are base64 encoded
            base64.urlsafe_b64decode(password.encode())
            return True
        except:
            return False