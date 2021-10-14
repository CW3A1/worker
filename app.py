from flask import Flask, jsonify, request
from database import *
import requests
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

@app.route('/api/column/<column>')
def showColumn(column):
    if column=="all":
        return jsonify(selectAll())
    return jsonify(selectAllColumn(column))

@app.route('/api/push', methods=["POST"])
def insertDatabase():
    insertIntoTable([request.json['id'], request.json['status']])
    return jsonify(selectAll())

@app.route('/api/pushurl/<id>/<status>')
def pushJSONtoDB(id, status):
    requests.post('http://' + request.host + '/api/push', json={"id": int(id), "status": int(status)})
    return jsonify(selectAll())