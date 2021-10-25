import uuid
from datetime import datetime, timedelta

from flask import (Flask, jsonify, make_response, redirect, render_template,
                   request, url_for)

import auth
import database
import environment
import openfoam

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

# JINJA FILTERS
@app.template_filter('human_time')
def human_time(s):
    dt = datetime.fromtimestamp(int(s) // 1000000000)
    t = dt.strftime(f'%Y-%m-%d %H:%M:%S')
    return t

@app.template_filter('human_status')
def human_time(s):
    s = int(s)
    if s == 0:
        return 'Created'
    elif s == 1:
        return 'Complete'
    elif s == 2:
        return 'Pending'
    return 'Unknown'

@app.template_filter('human_scheduler_status')
def human_time(s):
    s = int(s)
    if s == 0:
        return 'Free'
    elif s == 1:
        return 'Busy'
    return 'Unknown'

# EXTRA
@app.after_request
def securityHeaders(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5000")
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:11000")
    response.headers.add("Access-Control-Allow-Origin", "https://pno3cwa1.student.cs.kuleuven.be")
    return response

@app.errorhandler(404)
def not_found():
    return render_template("404.html")

@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

@app.route("/")
def tasks():
    return render_template("tasks.html", title='Tasks', task_data=database.list_task('all'))

@app.route("/task/<task_id>")
def view_task(task_id):
    if database.get_row(environment.DB_TABLE_TASKS, "task_id", task_id):
        return render_template("view_task.html", title=f'Task info', task_id=task_id, task_data=database.status_task(task_id))
    return render_template("404.html")

@app.route("/schedulers")
def schedulers():
    return render_template("schedulers.html", title='Schedulers', schedulers_data=database.list_scheduler())

@app.route("/users")
def users():
    return render_template("users.html", title='Users', user_data=database.select_all_column('uuid', environment.DB_TABLE_USERS))

@app.route("/users/<identifier>")
def view_user(identifier):
    if database.get_row(environment.DB_TABLE_USERS, "uuid", identifier):
        return render_template("view_user.html", title=f'Task info', user_data=database.user_info("uuid", identifier), task_data=database.list_task(identifier))
    return render_template("404.html")

# TASK ENDPOINTS
@app.route('/api/task/add', methods=["POST"])
def add_task():
    task_id = str(uuid.uuid4())[:8]
    r = request.json
    r = [float(r[x][0]) for x in r] + [float(r[x][1]) for x in r]
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header[:7] == 'Bearer ':
            jwt = auth_header[7:]
            if database.get_row(environment.DB_TABLE_USERS, "jwt_token", jwt):
                identifier = database.user_info("jwt_token", jwt)["uuid"]
                resp = database.add_task(task_id, r, identifier)
                openfoam.next_openfoam_thread()
                return jsonify(resp)
            return jsonify({"error": "token does not exist"})
        return jsonify({"error": "authorization header is malformed"})
    resp = database.add_task(task_id, r)
    openfoam.next_openfoam_thread()
    return jsonify(resp)

@app.route('/api/task/status/<task_id>')
def status_task(task_id):
    if database.get_row(environment.DB_TABLE_TASKS, "task_id", task_id):
        resp = database.status_task(task_id)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header[:7] == 'Bearer ':
                jwt = auth_header[7:]
                if database.get_row(environment.DB_TABLE_USERS, "jwt_token", jwt):
                    identifier = database.user_info("jwt_token", jwt)["uuid"]
                    if identifier == resp[task_id]['uuid']:
                        return jsonify(resp)
                    return jsonify({"error": "token does not match task"})
                return jsonify({"error": "token does not exist"})
            return jsonify({"error": "authorization header is malformed"})
        if resp[task_id]['uuid'] == '':
            return jsonify(resp)
        return jsonify({"error": "authorization is required"})
    return jsonify({"error": "task does not exist"})

# SCHEDULER ENDPOINTS
@app.route('/api/scheduler/free/<pc>')
def free_scheduler(pc):
    return jsonify(database.free_scheduler(pc))

@app.route('/api/scheduler/busy/<pc>')
def busy_scheduler(pc):
    return jsonify(database.busy_scheduler(pc))

# USER ENDPOINTS
@app.route('/api/user/add', methods=['POST'])
def add_user():
    email, password = request.json["email"], request.json["password"]
    resp = auth.add_user(email, password)
    if type(resp) == dict:
        return jsonify(resp)
    resp = auth.auth_user(email, password)
    return jsonify(resp)

@app.route('/api/user/auth', methods=['POST'])
def auth_user():
    email, password = request.json["email"], request.json["password"]
    resp = auth.auth_user(email, password)
    return jsonify(resp)

@app.route('/api/user/tasks')
def user_tasks():
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header[:7] == 'Bearer ':
            jwt = auth_header[7:]
            if database.get_row(environment.DB_TABLE_USERS, "jwt_token", jwt):
                identifier = database.user_info("jwt_token", jwt)["identifier"]
                return jsonify(database.list_task(identifier))
            return jsonify({"error": "token does not exist"})
        return jsonify({"error": "authorization header is malformed"})
    return redirect(url_for('list_task'))
