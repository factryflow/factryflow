FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
apt-get install -y netcat && \
apt-get install -y make

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# copy project
COPY src/ .
WORKDIR /app/src

RUN mkdir staticfiles
COPY ./Makefile .

ENTRYPOINT ["/app/entrypoint.sh"]
