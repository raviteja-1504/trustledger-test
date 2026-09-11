"""
Configuration file with intentional hardcoded secrets for SAST testing.
"""
import os

# VULNERABILITY: Hardcoded database credentials
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'username': 'admin',
    'password': 'SuperSecretDBPassword123!',  # Hardcoded secret
    'database': 'prod_db'
}

# VULNERABILITY: API keys in source code
AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
STRIPE_SECRET_KEY = 'sk_live_1234567890abcdef'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

# VULNERABILITY: Encryption key in source code
ENCRYPTION_KEY = 'this-is-a-weak-encryption-key'

# VULNERABILITY: JWT secret in source code
JWT_SECRET = 'secret-key-change-in-production'

# VULNERABILITY: Default admin credentials
DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'changeme123'  # Weak default password

def get_database_connection():
    """Return database connection using hardcoded credentials."""
    import psycopg2
    conn = psycopg2.connect(
        host=DATABASE_CONFIG['host'],
        port=DATABASE_CONFIG['port'],
        user=DATABASE_CONFIG['username'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database']
    )
    return conn