import sympy as sym
from sympy.printing.latex import latex

from modules.gen import *


def sym_diff(task_id: str, function: str, order: int):
    try:
        symfunc = parseString(function)
        for i in range(order):
            symfunc = sym.diff(symfunc)
        result = {'result': latex(symfunc)}
        add_log(f"Calculated symbolic derivative for task {task_id}")
    except:
        result = {'result': 'error'}
        add_log(f"Failed to calculate symbolic derivative for task {task_id}")
    finally:
        postToDB(task_id, result)

def sym_int(task_id: str, function: str):
    try:
        symfunc = parseString(function)
        a = sym.integrate(symfunc)
        result = {'result': latex(a)}
        add_log(f"Calculated symbolic integral for task {task_id}")
    except:
        result = {'result': 'error'}
        add_log(f"Failed to calculate symbolic integral for task {task_id}")
    finally:
        postToDB(task_id, result)

def sym_limit(task_id: str, function: str, x0: float, dir: int):
    try:
        symfunc = parseString(function)
        if dir == -1:
            a = sym.limit(symfunc,sym.Symbol('x'),x0, '-')
        elif dir == 1:
            a = sym.limit(symfunc,sym.Symbol('x'),x0, '+')
        else:
            a = sym.limit(symfunc,sym.Symbol('x'),x0)
        result = float(a)
        result = {"result": result}
        add_log(f"Calculated limit for task {task_id}")
    except:
        result = {'result': 'error'}
        add_log(f"Failed to calculate limit for task {task_id}")
    finally:
        postToDB(task_id, result)

def sym_solver(task_id: str, function: str):
    try:
        symfunc = parseString(function)
        result = [latex(i) for i in sym.solve(symfunc)]
        result = {"result": result}
        add_log(f"Calculated roots for task {task_id}")
    except:
        result = {'result': 'error'}
        add_log(f"Failed to calculate roots for task {task_id}")
    finally:
        postToDB(task_id, result)
