import uuid

from flask import Flask, jsonify, redirect, request, url_for

import auth
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
    r = [float(r[x][0]) for x in r] + [float(r[x][1]) for x in r]
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header[:7] == 'Bearer ':
            jwt = auth_header[7:]
            if database.jwt_exists(jwt):
                identifier = database.jwt_to_uuid(jwt)
                resp = database.add_task(task_id, r, identifier)
                openfoam.next_openfoam_thread()
                return corsonify(resp)
            return corsonify({"error": "token does not exist"})
        return corsonify({"error": "authorization header is malformed"})
    resp = database.add_task(task_id, r)
    openfoam.next_openfoam_thread()
    return corsonify(resp)

@app.route('/api/task/status/<task_id>')
def status_task(task_id):
    if database.task_exists(task_id):
        resp = database.status_task(task_id)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header[:7] == 'Bearer ':
                jwt = auth_header[7:]
                if database.jwt_exists(jwt):
                    identifier = database.jwt_to_uuid(jwt)
                    if identifier == resp[task_id]['uuid']:
                        return corsonify(resp)
                    return corsonify({"error": "token does not match task"})
                return corsonify({"error": "token does not exist"})
            return corsonify({"error": "authorization header is malformed"})
        if resp[task_id]['uuid'] == '':
            return corsonify(resp)
        return corsonify({"error": "authorization is required"})
    return corsonify({"error": "task does not exist"})

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

# USER ENDPOINTS
@app.route('/api/user/add', methods=['POST'])
def add_user():
    r = request.json
    if r['email'] and r['password']:
        identifier = auth.generate_uuid(r['email'])
        if not database.user_exists(identifier):
            hashed_password = auth.generate_hash(r['password'])
            jwt = auth.generate_jwt(identifier)
            return corsonify(database.add_user(identifier, hashed_password, jwt))
        return corsonify({"error": "user already exists"})
    return corsonify({"error": "invalid email or password"})

@app.route('/api/user/auth', methods=['POST'])
def auth_user():
    r = request.json
    if r['email'] and r['password']:
        identifier = auth.generate_uuid(r['email'])
        if database.user_exists(identifier):
            if auth.check_password(r['password'], database.user_hash(identifier)):
                return corsonify(database.user_info(identifier))
            return corsonify({"error": "wrong password"})
        return corsonify({"error": "user does not exist"})
    return corsonify({"error": "invalid email or password"})

@app.route('/api/user/tasks')
def user_tasks():
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header[:7] == 'Bearer ':
            jwt = auth_header[7:]
            if database.jwt_exists(jwt):
                identifier = database.jwt_to_uuid(jwt)
                return corsonify(database.list_task(identifier))
            return corsonify({"error": "token does not exist"})
        return corsonify({"error": "authorization header is malformed"})
    return redirect(url_for('list_task'))
