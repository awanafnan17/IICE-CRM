from django.core.management.base import BaseCommand
from IICE.email_encryption import EmailPasswordEncryption
import os

class Command(BaseCommand):
    help = 'Encrypt email password for secure storage'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            help='The email password to encrypt',
            required=False
        )
        parser.add_argument(
            '--generate-key',
            action='store_true',
            help='Generate a new encryption key'
        )
    
    def handle(self, *args, **options):
        if options['generate_key']:
            key = EmailPasswordEncryption.generate_key()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Generated encryption key: {key.decode()}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Add this key to your .env file as EMAIL_ENCRYPTION_KEY=<key>'
                )
            )
            return
        
        password = options['password']
        if not password:
            self.stdout.write(
                self.style.ERROR(
                    'Password is required when not generating a key. Use --password "your-password"'
                )
            )
            return
        
        # Check if encryption key exists
        if not os.environ.get('EMAIL_ENCRYPTION_KEY'):
            self.stdout.write(
                self.style.ERROR(
                    'EMAIL_ENCRYPTION_KEY not found in environment variables.'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Run: python manage.py encrypt_email_password --generate-key'
                )
            )
            return
        
        try:
            encrypted_password = EmailPasswordEncryption.encrypt_password(password)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Encrypted password: {encrypted_password}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Add this to your .env file as EMAIL_HOST_PASSWORD_ENCRYPTED=<encrypted_password>'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Remove the plain text EMAIL_HOST_PASSWORD from your .env file for security'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error encrypting password: {e}'
                )
            )