from scipy.optimize import dual_annealing
from sympy.abc import x, y

from modules.complete_task import postResp
from modules.gen import *


def twoDNumOpt(task_id: str, f: str, x_l=-512, x_u=512, y_l=-512, y_u=512):
    bounds = [(x_l, x_u),(y_l, y_u)]
    f = evalString(f, free_vars={x, y})
    def fun(z):
        nonlocal f
        return f(z[0], z[1])
    res = dual_annealing(fun, bounds)
    resp = {"vector": list(res.x) + [res.fun]}
    postResp(task_id, resp)
