from sympy import *
from sympy.abc import x
from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdastr
import math
from scipy.misc import derivative

init_printing(use_unicode=True)

string = '(sin(x)+1)**x'
eval_string = parse_expr(string)
f = eval(lambdastr(x, eval_string))

print(f(5))

print(float(derivative(f, 3*pi/2)))

