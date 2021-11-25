from typing import List

from scipy.integrate import quad
from scipy.interpolate import approximate_taylor_polynomial, lagrange
from scipy.misc import derivative
from scipy.optimize import dual_annealing
from sympy.abc import x, y

from modules.gen import *

def numDiff(task_id: str, f: str, a: float, o: int = 1):
    f = evalString(f)
    result = derivative(f, a, n=o, order=max(o+1+(o)%2, 7))
    result = {"result": result}
    postResp(task_id, result)

def numInt(task_id: str, f: str, a: float, b: float):
    f = evalString(f)
    result = quad(f, a, b)
    result = {"result": result[0], "err": result[1]}
    postResp(task_id, result)

def twoDNumOpt(task_id: str, f: str, x_l=-512, x_u=512, y_l=-512, y_u=512):
    bounds = [(x_l, x_u),(y_l, y_u)]
    f = evalString(f, free_vars={x, y})
    def fun(z):
        nonlocal f
        return f(z[0], z[1])
    res = dual_annealing(fun, bounds)
    resp = {"vector": list(res.x) + [res.fun]}
    postResp(task_id, resp)

def lagrangePoly(task_id: str, a: List[float], b: List[float]):
    poly_lagrange = lagrange(numpy.array(a), numpy.array(b))
    poly_lagrange_string = oneDPolyToStr(poly_lagrange)
    resp = {"result": poly_lagrange_string}
    postResp(task_id, resp)

def approximateTaylorPoly(task_id: str, f: str, x0: float, degree: int):
    poly = evalString(f)
    poly_taylor = approximate_taylor_polynomial(poly, x0, degree, 1, order=max(degree+2, 7))
    poly_taylor_string = oneDPolyToStr(poly_taylor)
    resp = {"result": poly_taylor_string}
    postResp(task_id, resp)