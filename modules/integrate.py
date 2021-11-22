from scipy.integrate import quad

from modules.complete_task import postResp
from modules.gen import *


def numInt(task_id: str, f: str, a: float, b: float):
    f = evalString(f)
    result = quad(f, a, b)
    result = {"result": result[0], "err": result[1]}
    postResp(task_id, result)
