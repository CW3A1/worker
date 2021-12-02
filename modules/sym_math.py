import sympy as sym

def sym_diff(function, order):
    symfunc = sym.sympify(function)
    i = 1
    while i<=order:
        a = sym.diff(symfunc)
        symfunc = a
        i += 1
    return symfunc

def sym_int(function):
    symfunc = sym.sympify(function)
    a = sym.integrate(symfunc)
    return a

def sym_limit(function,x0,dir=0):
    symfunc = sym.sympify(function)
    if dir == '-' or dir == '+':
         a = sym.limit(symfunc,sym.Symbol('x'),x0,dir)
    else:
        a = sym.limit(symfunc,sym.Symbol('x'),x0)
    return a

def sym_solver(function):
    symfunc = sym.sympify(function)
    a = sym.solve(symfunc)
    return a

