FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["hypercorn", "app:app", "--worker-class", "trio", "-b", "0.0.0.0:11002"]