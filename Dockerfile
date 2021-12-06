# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
# SETUP PYTHON ENV
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
# RUN FLASK
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:11002", "app:app"]