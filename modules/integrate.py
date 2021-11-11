from scipy.integrate import quad

from modules.gen import *


def numInt(f: str, a: float, b: float):
    f = evalString(f)
    result = quad(f, a, b)
    return {"result": result[0], "error": result[1]}
