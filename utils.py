"""
Utility functions with intentional vulnerabilities for SAST testing.
"""

import os
import subprocess
import yaml
import json
import re

# VULNERABILITY: Hardcoded API key
API_KEY = 'sk_live_1234567890abcdef'

def process_user_input(data):
    """Process user input with multiple vulnerabilities."""

    # VULNERABILITY: eval on user input
    if 'expression' in data:
        result = eval(data['expression'])
        print(f"Eval result: {result}")

    # VULNERABILITY: Unsafe YAML loading
    if 'yaml_data' in data:
        parsed = yaml.load(data['yaml_data'], Loader=yaml.Loader)
        print(f"YAML parsed: {parsed}")

    # VULNERABILITY: Regular expression denial of service (ReDoS) potential
    if 'pattern' in data and 'text' in data:
        # Dangerous pattern that could cause ReDoS
        pattern = data['pattern']
        text = data['text']
        match = re.search(pattern, text)
        if match:
            print(f"Pattern matched: {match.group()}")

    # VULNERABILITY: Shell injection via subprocess
    if 'command' in data:
        cmd = f"echo {data['command']}"
        subprocess.run(cmd, shell=True)

    return "Processing complete"

def insecure_password_check(password):
    """Insecure password checking with timing attack vulnerability."""
    # VULNERABILITY: Timing attack - string comparison not constant time
    stored_password = "SuperSecret123!"
    return password == stored_password

def weak_encryption(text):
    """Weak encryption using XOR with short key."""
    # VULNERABILITY: Weak custom encryption
    key = 0x42
    encrypted = ''.join(chr(ord(c) ^ key) for c in text)
    return encrypted

def log_sensitive_data(data):
    """Log sensitive data without proper sanitization."""
    # VULNERABILITY: Log injection and sensitive data exposure
    log_entry = f"User data: {data}"
    with open('app.log', 'a') as f:
        f.write(log_entry + '\n')

    # Also print to console (sensitive data exposure)
    print(f"DEBUG: {log_entry}")

def parse_json_safely(json_str):
    """Parse JSON with a vulnerability."""
    # This function appears safe but has a subtle issue
    data = json.loads(json_str)

    # VULNERABILITY: JSON injection if data is later serialized unsafely
    return data