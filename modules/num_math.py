from time import time
from typing import List

import matplotlib.pyplot as plt
from numpy import array, linspace, vectorize
from scipy.integrate import quad
from scipy.interpolate import approximate_taylor_polynomial, lagrange
from scipy.misc import derivative
from scipy.optimize import dual_annealing
from scipy.special import factorial
from sympy import Float, preorder_traversal, simplify
from sympy.abc import *

from modules.gen import *


def numDiff(task_id: str, f: str, a: float, o: int = 1):
    try:
        f = evalString(f)
        result = derivative(f, a, n=o, order=max(o+1+(o)%2, 7))
        add_log(f"Calculated derivative for task {task_id}")
        try:
            link = plotDiff(f, a, o)
            add_log(f"Generated plot for for task {task_id}")
        except:
            link = "error"
            add_log(f"Failed to generate plot for task {task_id}")
        result = {"result": result, "link": link}
    except:
        result = {"result": "error", "link": "error"}
        add_log(f"Failed to calculate derivative for task {task_id}")
    finally:
        postToDB(task_id, result)

def numInt(task_id: str, f: str, a: float, b: float):
    try:
        f = evalString(f)
        result = quad(f, a, b)
        add_log(f"Calculated integral for task {task_id}")
        try:
            link = plotIntegral(f, a, b)
            add_log(f"Generated plot for task {task_id}")
        except:
            link = "error"
            add_log(f"Failed to generate plot for task {task_id}")
        result = {"result": result[0], "err": result[1], "link": link}
    except:
        result = {"result": "error", "err": "error", "link": "error"}
        add_log(f"Failed to calculate integral for task {task_id}")
    finally:
        postToDB(task_id, result)

def twoDNumOpt(task_id: str, f: str, x_l=-512, x_u=512, y_l=-512, y_u=512):
    try:
        bounds = [(x_l, x_u),(y_l, y_u)]
        f = evalString(f, free_vars={x, y})
        def fun(z):
            nonlocal f
            return f(z[0], z[1])
        res = dual_annealing(fun, bounds)
        result = {"vector": list(res.x) + [res.fun]}
        add_log(f"Calculated global minimum for task {task_id}")
    except:
        result = {"result": "error"}
        add_log(f"Failed to calculate global minimum for task {task_id}")
    finally:
        postToDB(task_id, result)


def lagrangePoly(task_id: str, a: List[float], b: List[float]):
    try:
        poly_lagrange = lagrange(array(a), array(b))
        poly_lagrange_string = oneDPolyToStr(poly_lagrange)
        add_log(f"Calculated Lagrange polynomial for task {task_id}")
        try:
            link = plotLagrange(poly_lagrange_string, a, b)
            add_log(f"Generated plot for for task {task_id}")
        except:
            link = "error"
            add_log(f"Failed to generate plot for task {task_id}")
        result = {"result": poly_lagrange_string, "link": link}
    except:
        result = {"result": "error", "link": "error"}
        add_log(f"Failed to calculate Lagrange polynomial for task {task_id}")
    finally:
        postToDB(task_id, result)

def approximateTaylorPoly(task_id: str, f: str, x0: float, degree: int):
    try:
        poly = evalString(f)
        poly_taylor = approximate_taylor_polynomial(poly, x0, degree, 1, order=max(degree+2, 7))
        poly_taylor_string = oneDPolyToStr(poly_taylor)
        add_log(f"Calculated Taylor approximation for task {task_id}")
        try:
            link = plotTaylor(f, poly_taylor_string, x0)
            add_log(f"Generated plot for for task {task_id}")
        except:
            link = "error"
            add_log(f"Failed to generate plot for task {task_id}")
        result = {"result": poly_taylor_string, "link": link}
    except:
        result = {"result": "error", "link": "error"}
        add_log(f"Failed to calculate Taylor approximation for task {task_id}")
    finally:
        postToDB(task_id, result)

def plotDiff(f: str, a: float, o: int):
    fun = evalString(f)
    dx = linspace(start=0 if a>0 else (2 * a if a < 0 else -10), stop=2*a if a>0 else (0 if a < 0 else 10), num=100)
    if o == 1:
        differentiaal = derivative(fun, a, n=o, order=max(o+1+(o)%2, 7))
        f0 = fun(a)
        raaklijn = lambda x: (f0 - differentiaal * a) + differentiaal * x
        raaklijn_vector = vectorize(raaklijn)
        raaklijn = raaklijn_vector(dx)
        plt.plot(dx, raaklijn, '#1f2937')
        legend_approximation = "Tangent line in given point"
    else:
        afgeleide = []
        for i in dx[1:len(dx) - 1]:
            afgeleide.append(derivative(f, i, n=o, order=max(o+1+(o)%2, 7)))
        plt.plot(dx[1: len(dx) - 1], afgeleide, '#1f2937')
        legend_approximation = "Derivative"
        a_vector = [a] * 5
        f_accent_a = afgeleide[len(afgeleide) // 2]
        if f_accent_a > 0:
            vert_points = numpy.linspace(0, f_accent_a, num=5)
        else:
            vert_points = numpy.linspace(f_accent_a, 0, num=5)
        plt.plot(a_vector, vert_points, color='r')
    f_vector = vectorize(f)
    f = f_vector(dx)
    plt.plot(dx, f, '#5599ff')
    plt.xlabel("X-axis")
    plt.ylabel('Y-axis')
    plt.title('Derivative')
    if o == 1:
        plt.legend([legend_approximation, 'Original function'])
    else:
        plt.legend([legend_approximation, 'Derivative in chosen point', 'Original function'])
        plt.scatter(a, f_accent_a, color='r', linewidths=0.01)
    f = f"/tmp/{time()}.png"
    plt.savefig(f)
    link = uploadToUguu(f)
    return link

def plotIntegral(f, a: float, b: float):
    x_begin = a - (b-a)*0.2
    x_eind = b + (b-a)*0.2
    dx_lang = numpy.linspace(start=x_begin, stop= x_eind, num = 51)
    dx_kort = numpy.linspace(start=a, stop=b, num = 51)
    plot = plt.figure()
    plt.plot(dx_lang, f(dx_lang), '#1f2937')
    plt.fill_between(dx_kort, f(dx_kort), y2=0, color= '#5599ff')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend(['Integrand', 'Value of integral'])
    plt.title('Integral of given function')
    f = f"/tmp/{time()}.png"
    plt.savefig(f)
    link = uploadToUguu(f)
    return link

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

def plotTaylor(f: str, a: float, o: int):
    fun = evalString(f)
    taylor = fun(a)
    for i in range(1, o+1):
        taylor = taylor + derivative(fun, a, n=i, order=max(o+1+o%2, 7))*(x-a)**i/factorial(i)
    taylor = simplify(taylor)
    taylor_round = taylor
    for r in preorder_traversal(taylor):
        if isinstance(r, Float):
            taylor_round = taylor_round.subs(r, round(r, 1))
    taylor_lambda = lambdify(x, taylor_round)
    dx = linspace(start=0 if a>0 else (2*a if a<0 else -10), stop=2*a if a>0 else (0 if a<0 else 10), num = 100)
    f_vector = vectorize(f)
    taylor_vector = vectorize(taylor_lambda)
    taylor = taylor_vector(dx)
    fv = f_vector(dx)
    plt.plot(dx, taylor, color = "#1f2937")
    plt.plot(dx, fv, color = "#5599ff")
    plt.scatter(a,f(a),color='r')
    plt.xlabel("X-axis")
    plt.ylabel('Y-axis')
    plt.title('Taylor approximation')
    plt.legend(['Taylor approximation','Original function'])
    plt.show()
    f = f"/tmp/{time()}.png"
    plt.savefig(f)
    link = uploadToUguu(f)
    return link
