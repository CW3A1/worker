from flask import Flask, jsonify, redirect, url_for
import uuid, database, environment

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

@app.route('/api/<table>/<column>')
def showColumn(table, column):
    if column=="all":
        return jsonify(database.selectAll(table))
    return jsonify(database.selectAllColumn(column, table))

@app.route('/api/addTask')
def addTask():
    task_id = str(uuid.uuid4())[:8]
    database.addTask(task_id)
    return redirect(url_for('statusTask', task_id=task_id))

@app.route('/api/completeTask/<task_id>')
def completeTask(task_id):
    database.completeTask(task_id)
    return redirect(url_for('statusTask', task_id=task_id))

@app.route('/api/statusTask/<task_id>')
def statusTask(task_id):
    return jsonify(database.statusTask(task_id))

# @app.route('/api/pushurl/<id>/<status>')
# def pushJSONtoDB(id, status):
#     if request.args.get('secret')==environment.db_secret:
#         if id not in (None, "") and status not in (0, 1):
#             resp = requests.get(f"{environment.db_url}/api/column/id")
#             print(id, resp.json(), id not in resp.json())
#             if id not in resp.json():
#                 requests.post(f"{environment.db_url}/api/push", json={"id": int(id), "status": int(status)})
#                 return redirect(url_for('showAPI'))
#             return jsonify({"error": "id must be unique"})
#         return jsonify({"error": "invalid id or status provided"})
#     return jsonify({"error": "invalid secret provided"})