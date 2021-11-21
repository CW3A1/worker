from scipy.interpolate import approximate_taylor_polynomial

from modules.complete_task import postResp
from modules.gen import *


def approximateTaylorPoly(task_id: str, f: str, x0: float, degree: int):
    poly = evalString(f)
    poly_taylor = approximate_taylor_polynomial(poly, x0, degree, 1, order=max(degree+2, 7))
    poly_taylor_string = oneDPolyToStr(poly_taylor)
    resp = {"result": poly_taylor_string}
    postResp(task_id, resp)
