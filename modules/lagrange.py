from typing import List

from scipy.interpolate import lagrange

from modules.complete_task import postResp
from modules.gen import *


def lagrangePoly(task_id: str, a: List[float], b: List[float]):
    poly_lagrange = lagrange(numpy.array(a), numpy.array(b))
    poly_lagrange_string = oneDPolyToStr(poly_lagrange)
    resp = {"result": poly_lagrange_string}
    postResp(task_id, resp)
