# Email Password Encryption Guide

This guide explains how to securely encrypt your email password in the IICE-CRM application.

## Why Encrypt Email Passwords?

- **Security**: Prevents exposure of sensitive email credentials in configuration files
- **Production Safety**: Reduces risk if configuration files are accidentally committed to version control
- **Compliance**: Meets security best practices for handling sensitive data

## Setup Instructions

### Step 1: Generate an Encryption Key

Run the following command to generate a new encryption key:

```bash
python manage.py encrypt_email_password --generate-key
```

This will output something like:
```
Generated encryption key: gAAAAABhZ1234567890abcdefghijklmnopqrstuvwxyz==
```

### Step 2: Add the Key to Your Environment

Add the generated key to your `.env` file:

```env
EMAIL_ENCRYPTION_KEY=gAAAAABhZ1234567890abcdefghijklmnopqrstuvwxyz==
```

### Step 3: Encrypt Your Email Password

Run the following command with your actual email password:

```bash
python manage.py encrypt_email_password --password "your-actual-email-password"
```

This will output something like:
```
Encrypted password: Z0FBQUFBQmhaMTIzNDU2Nzg5MGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6PT0=
```

### Step 4: Update Your Environment File

Add the encrypted password to your `.env` file and remove the plain text password:

```env
# Remove this line (if it exists):
# EMAIL_HOST_PASSWORD=your-plain-text-password

# Add this line instead:
EMAIL_HOST_PASSWORD_ENCRYPTED=Z0FBQUFBQmhaMTIzNDU2Nzg5MGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6PT0=
```

## Configuration Options

The application supports both encrypted and plain text passwords for backward compatibility:

### Option 1: Encrypted Password (Recommended)
```env
EMAIL_ENCRYPTION_KEY=your-encryption-key
EMAIL_HOST_PASSWORD_ENCRYPTED=your-encrypted-password
```

### Option 2: Plain Text Password (Development Only)
```env
EMAIL_HOST_PASSWORD=your-plain-text-password
```

## Security Best Practices

1. **Never commit encryption keys to version control**
2. **Use encrypted passwords in production environments**
3. **Store encryption keys securely** (e.g., in environment variables or secure key management systems)
4. **Rotate encryption keys periodically**
5. **Use different keys for different environments** (development, staging, production)

## Troubleshooting

### Error: "EMAIL_ENCRYPTION_KEY not found"
- Make sure you've added the encryption key to your `.env` file
- Verify the key is properly formatted (no extra spaces or characters)

### Error: "Error decrypting password"
- Check that the encrypted password was generated with the same encryption key
- Verify both the key and encrypted password are correctly copied to your `.env` file

### Fallback Behavior
- If decryption fails, the system will fall back to using the encrypted string as a plain text password
- This ensures backward compatibility but may cause authentication failures

## Migration from Plain Text

If you're currently using plain text passwords:

1. Generate an encryption key
2. Encrypt your existing password
3. Update your `.env` file with the encrypted version
4. Remove the plain text password
5. Test email functionality to ensure everything works

## Example Complete Setup

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Encryption Setup
EMAIL_ENCRYPTION_KEY=gAAAAABhZ1234567890abcdefghijklmnopqrstuvwxyz==
EMAIL_HOST_PASSWORD_ENCRYPTED=Z0FBQUFBQmhaMTIzNDU2Nzg5MGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6PT0=
```

After setup, your email functionality will work exactly as before, but with enhanced security!