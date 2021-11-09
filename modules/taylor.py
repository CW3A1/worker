from scipy.interpolate import approximate_taylor_polynomial

from modules.gen import *

def approximateTaylorPoly(f: str, x0: float, degree: int):
    poly = oneDEvalString(f)
    poly_taylor = approximate_taylor_polynomial(poly, x0, degree, 1, order=degree+2)
    poly_taylor_string = oneDPolyToStr(poly_taylor)
    return poly_taylor_string
