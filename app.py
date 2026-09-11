#!/usr/bin/env python3
"""
Intentionally vulnerable Flask application for SAST testing.
Contains multiple security vulnerabilities for detection by SAST tools.
"""

import os
import sqlite3
import pickle
import hashlib
import random
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# VULNERABILITY: Hardcoded secret key
app.config['SECRET_KEY'] = 'super-secret-key-12345'

# Simple in-memory database setup
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    return conn

DB_CONN = init_db()

@app.route('/')
def index():
    return '''
    <h1>Vulnerable App for SAST Testing</h1>
    <ul>
        <li><a href="/sqli?user=admin">SQL Injection Example</a></li>
        <li><a href="/cmd?file=whoami">Command Injection Example</a></li>
        <li><a href="/xss?name=Visitor">XSS Example</a></li>
        <li><a href="/traverse?file=README.md">Path Traversal Example</a></li>
        <li><a href="/deserialize">Insecure Deserialization Example</a></li>
        <li><a href="/hash?data=test">Weak Cryptography Example</a></li>
        <li><a href="/debug">Sensitive Data Exposure Example</a></li>
        <li><a href="/token">Insecure Randomness Example</a></li>
    </ul>
    '''

@app.route('/sqli')
def sqli():
    # VULNERABILITY: SQL Injection - user input directly concatenated
    username = request.args.get('user', '')
    cursor = DB_CONN.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    return f'SQL Query: {query}<br>Result: {result}'

@app.route('/cmd')
def cmd():
    # VULNERABILITY: Command Injection - unsanitized input passed to os.system
    filename = request.args.get('file', '')
    output = os.popen(f'ls -la {filename}').read()
    return f'Command output: <pre>{output}</pre>'

@app.route('/xss')
def xss():
    # VULNERABILITY: Cross-Site Scripting - unsanitized user input in template
    name = request.args.get('name', '')
    template = f'<h1>Hello, {name}!</h1><p>Welcome to our site.</p>'
    return render_template_string(template)

@app.route('/traverse')
def traverse():
    # VULNERABILITY: Path Traversal - user input used to construct file path
    file_param = request.args.get('file', '')
    base_dir = '/home/user/files/'
    file_path = os.path.join(base_dir, file_param)
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return f'File content: <pre>{content}</pre>'
    except Exception as e:
        return f'Error reading file: {e}'

@app.route('/deserialize', methods=['POST', 'GET'])
def deserialize():
    # VULNERABILITY: Insecure Deserialization - pickle.loads on untrusted data
    if request.method == 'POST':
        data = request.form.get('data', '')
        try:
            obj = pickle.loads(bytes.fromhex(data))
            return f'Deserialized object: {obj}'
        except Exception as e:
            return f'Deserialization error: {e}'
    return '''
    <form method="POST">
        <label>Enter hex-encoded pickle data:</label><br>
        <input type="text" name="data"><br>
        <input type="submit" value="Deserialize">
    </form>
    '''

@app.route('/hash')
def weak_hash():
    # VULNERABILITY: Weak Cryptography - using MD5 (cryptographically broken)
    data = request.args.get('data', '')
    md5_hash = hashlib.md5(data.encode()).hexdigest()
    return f'MD5 hash of "{data}": {md5_hash}'

@app.route('/debug')
def debug_info():
    # VULNERABILITY: Sensitive Data Exposure - debug information leakage
    debug_data = {
        'app_config': dict(app.config),
        'request_headers': dict(request.headers),
        'environment_vars': dict(os.environ)
    }
    return f'<pre>{debug_data}</pre>'

@app.route('/token')
def generate_token():
    # VULNERABILITY: Insecure Randomness - using random for security tokens
    token = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
    return f'Generated token: {token}'

@app.route('/validate')
def improper_validation():
    # VULNERABILITY: Improper Input Validation - no validation on user input
    user_id = request.args.get('id', '')
    # Assume user_id should be numeric, but no validation
    return f'User ID: {user_id}'

if __name__ == '__main__':
    # VULNERABILITY: Running with debug mode enabled in production-like scenario
    app.run(debug=True, host='0.0.0.0', port=5000)