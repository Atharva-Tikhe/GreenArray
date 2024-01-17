# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

# ARG PYTHON_VERSION=3.10.8
# FROM python:${PYTHON_VERSION}-slim as base

FROM python:3.10.0-alpine


# Prevents Python from writing pyc files.
# ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
# ENV PYTHONUNBUFFERED=1

WORKDIR /

# Copy the source code into the container.
COPY . .
ENV PYTHONUNBUFFERED=1
RUN apk add python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip 

RUN python -m pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 8080


# Run the application.
CMD python3 webapp/webapp/app.py
