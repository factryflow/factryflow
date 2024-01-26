# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements-dev.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run makemigrations and migrate when the container launches
CMD ["make", "migrations"]
CMD ["make", "migrate"]

# to sync all user roles
CMD ["make", "sync_roles"]

# to create superuser
CMD ["make", "superuser"]

# Command to start the Django development server
CMD ["make", "dev"]
