# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
# SETUP PYTHON ENV
COPY app.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
# SETUP DATABASE
RUN apt update
RUN apt install -y libsqlite3-dev sqlite3
COPY createDB.sql .
RUN sqlite3 sqlite.db < createDB.sql
COPY database.py .
# RUN FLASK
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=11001"]