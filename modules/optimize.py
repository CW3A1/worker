from typing import List

from pydantic.main import BaseModel
from scipy.optimize import dual_annealing

from modules.gen import *


class OptResult(BaseModel):
    vector: List[float]
    res: float

def twoDNumOpt(f="-(y+47)*sin(sqrt(abs(x/2+y+47)))-x*sin(sqrt(abs(x-y+47)))", x_l=-512, x_u=512, y_l=-512, y_u=512):
    bounds = [(x_l, x_u),(y_l, y_u)]
    f = twoDEvalString(f)
    def fun(z):
        nonlocal f
        return f(z[0], z[1])
    res = dual_annealing(fun, bounds)
    return OptResult(vector=list(res.x), res=res.fun)
