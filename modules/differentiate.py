from scipy.misc import derivative

from modules.gen import *


def numDiff(f: str, a: float, o: int = 1):
    f = evalString(f)
    result = derivative(f(y=0,z=0), a, n=o, order=o+1+(o)%2)
    return round(result, 5)
