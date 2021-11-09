from scipy.misc import derivative

from modules.gen import *


def numDiff(f: str, a: float, o: int = 1):
    f = oneDEvalString(f)
    result = derivative(f, a, n=o, order=o+1+(o)%2)
    return round(result, 5)
