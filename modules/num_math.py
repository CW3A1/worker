from time import time
from typing import List

import matplotlib.pyplot as plt
from numpy import array, linspace
from scipy.integrate import quad
from scipy.interpolate import approximate_taylor_polynomial, lagrange
from scipy.misc import derivative
from scipy.optimize import dual_annealing
from sympy.abc import *

from modules.gen import *


def numDiff(task_id: str, f: str, a: float, o: int = 1):
    f = evalString(f)
    result = derivative(f, a, n=o, order=max(o+1+(o)%2, 7))
    result = {"result": result}
    postToDB(task_id, result)

def numInt(task_id: str, f: str, a: float, b: float):
    f = evalString(f)
    result = quad(f, a, b)
    result = {"result": result[0], "err": result[1]}
    postToDB(task_id, result)

def twoDNumOpt(task_id: str, f: str, x_l=-512, x_u=512, y_l=-512, y_u=512):
    bounds = [(x_l, x_u),(y_l, y_u)]
    f = evalString(f, free_vars={x, y})
    def fun(z):
        nonlocal f
        return f(z[0], z[1])
    res = dual_annealing(fun, bounds)
    resp = {"vector": list(res.x) + [res.fun]}
    postToDB(task_id, resp)

def lagrangePoly(task_id: str, a: List[float], b: List[float]):
    poly_lagrange = lagrange(array(a), array(b))
    poly_lagrange_string = oneDPolyToStr(poly_lagrange)
    link = plotLagrange(poly_lagrange_string, a, b)
    resp = {"result": poly_lagrange_string, "link": link}
    postToDB(task_id, resp)

def approximateTaylorPoly(task_id: str, f: str, x0: float, degree: int):
    poly = evalString(f)
    poly_taylor = approximate_taylor_polynomial(poly, x0, degree, 1, order=max(degree+2, 7))
    poly_taylor_string = oneDPolyToStr(poly_taylor)
    link = plotTaylor(f, poly_taylor_string, x0)
    resp = {"result": poly_taylor_string, "link": link}
    postToDB(task_id, resp)

def plotLagrange(f: str, a: List[float], b: List[float]):
    fun = evalString(f)
    dx = linspace(start = min(a)-2, stop = max(a)+2, num = 51)
    plot = plt.figure()
    plt.scatter(a, b)
    plt.plot(dx, fun(dx))
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend(['Original points',
                'Interpolated function'])
    plt.title(f'Lagrange interpolation of given points')
    f = f"/tmp/{time()}.png"
    plt.savefig(f)
    link = uploadToUguu(f)
    return link

def plotTaylor(f1: str, f2: str, x0: float):
    fun_1 = evalString(f1)
    fun_2 = evalString(f2)
    dx = linspace(start = x0-5, stop = x0+5, num = 51)
    plot = plt.figure()
    plt.plot(dx, fun_1(dx))
    plt.plot(dx, fun_2(dx))
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend(['Original function',
                'Approximated function'])
    plt.title(f'Taylor approximation of {f1} around {x0}')
    f = f"/tmp/{time()}.png"
    plt.savefig(f)
    link = uploadToUguu(f)
    return link
