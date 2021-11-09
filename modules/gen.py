import math

import numpy as np
import scipy.special as special
from sympy import Poly, init_printing
from sympy.abc import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdify

init_printing(use_unicode=True)

def oneDEvalString(f: str):
    eval_string = parse_expr(f)
    f = lambdify((x), eval_string)
    return f

def twoDEvalString(f: str):
    eval_string = parse_expr(f)
    f = lambdify((x,y), eval_string)
    return f

def threeDEvalString(f: str):
    eval_string = parse_expr(f)
    f = lambdify((x,y,z), eval_string)
    return f

def oneDPolyToStr(f: np.poly1d):
    return str(Poly([round(num, 5) for num in f.coef], x).as_expr())
