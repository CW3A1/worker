from scipy.misc import derivative

from modules.complete_task import postResp
from modules.gen import *


def numDiff(task_id: str, f: str, a: float, o: int = 1):
    f = evalString(f)
    result = derivative(f, a, n=o, order=max(o+1+(o)%2, 7))
    result = {"result": result}
    postResp(task_id, result)
