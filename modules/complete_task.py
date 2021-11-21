from requests import post

from modules.environment import DB_URL


def postResp(task_id: str, res):
    post(DB_URL+"api/task/complete", json={"task_id": task_id, "data": res})
