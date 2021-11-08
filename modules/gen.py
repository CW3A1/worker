import math

import scipy.special as special
from sympy import *
from sympy.abc import x, y, z
from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdify

init_printing(use_unicode=True)

def evalString(f: str):
    eval_string = parse_expr(f)
    f = lambdify((x,y,z), eval_string)
    return f
