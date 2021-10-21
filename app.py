import uuid

from flask import Flask, jsonify, request

import database
import openfoam

app = Flask(__name__)

def corsonify(resp):
    jsonifiedResp = jsonify(resp)
    jsonifiedResp.headers.add("Access-Control-Allow-Origin", "*")
    return jsonifiedResp

# TASK ENDPOINTS
@app.route('/api/task/list')
def list_task():
    return corsonify(database.list_task())

@app.route('/api/task/add', methods=["POST"])
def add_task():
    task_id = str(uuid.uuid4())[:8]
    r = request.json
    r = {int(x):r[x] for x in r}
    resp = database.add_task(task_id, )
    openfoam.next_openfoam_thread()
    return corsonify(resp)

@app.route('/api/task/complete/<task_id>')
def complete_task(task_id):
    resp = database.complete_task(task_id)
    openfoam.next_openfoam_thread()
    return corsonify(resp)

@app.route('/api/task/status/<task_id>')
def status_task(task_id):
    return corsonify(database.status_task(task_id))

# SCHEDULER ENDPOINTS
@app.route('/api/scheduler/list')
def list_scheduler():
    return corsonify(database.list_scheduler())

@app.route('/api/scheduler/free/<pc>')
def free_scheduler(pc):
    return corsonify(database.free_scheduler(pc))

@app.route('/api/scheduler/busy/<pc>')
def busy_scheduler(pc):
    return corsonify(database.busy_scheduler(pc))

@app.route('/api/scheduler/status/<pc>')
def status_scheduler(pc):
    return corsonify(database.status_scheduler(pc))
