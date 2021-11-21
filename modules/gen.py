import numpy
from sympy import Poly, init_printing
from sympy.abc import *
from sympy.parsing.sympy_parser import (convert_xor,
                                        implicit_multiplication_application,
                                        parse_expr, standard_transformations)
from sympy.utilities.lambdify import lambdify

init_printing(use_unicode=True)

def evalString(f: str, free_vars: set = set()):
    parse_string = parse_expr(f, transformations=standard_transformations+(convert_xor, implicit_multiplication_application,))
    if len(free_vars) > 0:
        f = lambdify(free_vars, parse_string, "numpy")
    else:
        f = lambdify(parse_string.free_symbols, parse_string, "numpy")
    return f

def oneDPolyToStr(f: numpy.poly1d):
    return str(Poly([round(num, 5) for num in f.coef], x).as_expr())
