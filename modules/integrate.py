from pydantic.main import BaseModel
from scipy.integrate import quad

from modules.gen import *


class IntResult(BaseModel):
    result: float
    error: float


def numInt(f: str, a: float, b: float):
    f = evalString(f)
    result = quad(f(y=0,z=0), a, b)
    return IntResult(result=round(result[0], 5), error=round(result[1], 5))
