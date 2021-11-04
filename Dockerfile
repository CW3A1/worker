FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["hypercorn", "--bind", "0.0.0.0:11001", "app:app"]