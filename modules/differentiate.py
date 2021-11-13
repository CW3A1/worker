from scipy.misc import derivative

from modules.gen import *


def numDiff(f: str, a: float, o: int = 1):
    f = evalString(f)
    result = derivative(f, a, n=o, order=max(o+1+(o)%2, 7))
    return {"result": result}
