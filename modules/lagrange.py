from typing import List

from scipy.interpolate import lagrange

from modules.gen import *


def lagrangePoly(a: List[float], b: List[float]):
    poly_lagrange = lagrange(np.array(a), np.array(b))
    poly_lagrange_string = oneDPolyToStr(poly_lagrange)
    return poly_lagrange_string
