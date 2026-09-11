# Simple SAST Vulnerable Repository

This repository contains intentionally vulnerable code for testing SAST (Static Application Security Testing) tools. It includes up to 10 different vulnerability types that can be detected by tools like CodeQL, Opengrep, Bandit, DevSkim, and Checkov SAST.

## Vulnerabilities Included

1. **SQL Injection** - Unsanitized user input concatenated into SQL query
2. **Command Injection** - Unsanitized user input passed to `os.system()`
3. **Path Traversal** - User input used to construct file paths without validation
4. **Cross-Site Scripting (XSS)** - Unsanitized user input rendered in HTML
5. **Hardcoded Secrets** - API keys and passwords in source code
6. **Insecure Deserialization** - Using `pickle.loads()` on untrusted data
7. **Weak Cryptography** - Use of MD5 hash function
8. **Improper Input Validation** - Missing validation for user inputs
9. **Sensitive Data Exposure** - Debug information leakage
10. **Insecure Randomness** - Using `random` instead of `secrets` for tokens

## Project Structure

- `app.py` - Main Flask application with vulnerabilities
- `utils.py` - Utility functions with additional vulnerabilities
- `config.py` - Configuration with hardcoded secrets
- `templates/` - HTML templates with XSS vulnerability
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration with security issues
- `terraform/` - Terraform files for Checkov SAST testing

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. The app will be available at `http://localhost:5000`

**WARNING**: This code is intentionally vulnerable. Do not deploy in production environments.

## Testing with SAST Tools

- **Bandit**: `bandit -r .`
- **CodeQL**: Create database and run queries
- **Opengrep**: Use patterns to detect vulnerabilities
- **DevSkim**: Run against codebase
- **Checkov SAST**: `checkov --directory .`

Each vulnerability is marked with a comment `# VULNERABILITY: [type]` for easy identification.