FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Copy both production and development requirements files
COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements-dev.txt

# Install development dependencies (which includes production dependencies)
RUN pip install -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements.txt /tmp/requirements-dev.txt
