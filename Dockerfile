FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Set the working directory in the container
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

# Update package lists and install make
RUN apt-get update && \
    apt-get install -y make

# RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy the current directory contents into the container at /app
COPY . .


# System deps:
RUN pip install -r requirements-dev.txt


# Expose port 8000 to the outside world
EXPOSE 8000

# Run makemigrations and migrate when the container launches
RUN make migrations
RUN make migrate

# to sync all user roles
RUN make sync_roles

# to create superuser
RUN make superuser

# Command to start the Django development server
CMD ["make", "dev"]
