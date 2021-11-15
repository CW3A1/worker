from typing import List

from scipy.interpolate import lagrange

from modules.gen import *


def lagrangePoly(a: List[float], b: List[float]):
    poly_lagrange = lagrange(numpy.array(a), numpy.array(b))
    poly_lagrange_string = oneDPolyToStr(poly_lagrange)
    return {"result": poly_lagrange_string}
