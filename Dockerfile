# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
# SETUP PYTHON ENV
COPY requirements.txt .
RUN pip3 install -r requirements.txt
# RUN FLASK
COPY . .
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=11001"]