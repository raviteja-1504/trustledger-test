# VULNERABILITY: Using latest tag
FROM python:latest

# VULNERABILITY: Running as root
USER root

# VULNERABILITY: Copying all files (including secrets)
COPY . /app
WORKDIR /app

# VULNERABILITY: Installing with root privileges
RUN pip install --no-cache-dir -r requirements.txt

# VULNERABILITY: Exposing all ports
EXPOSE 5000

# VULNERABILITY: Running as root
CMD ["python", "app.py"]