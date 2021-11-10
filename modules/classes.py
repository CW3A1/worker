from typing import Dict, List

from pydantic import BaseModel


# OPTIONS
class DiffOptions(BaseModel):
    f: str = "sin(x)"
    a: float = 0
    order: int = 1

class IntOptions(BaseModel):
    f: str = "sin(x)"
    a: float = -1
    b: float = 1

class OptimOptions(BaseModel):
    f: str = "sin(x)"
    xl: float = -1
    xu: float = 1
    yl: float = -1
    yu: float = 1

class LagrangeOptions(BaseModel):
    a: List[float]
    b: List[float]

class TaylorOptions(BaseModel):
    f: str = "sin(x)"
    x0: float = 0
    order: int = 1

# INPUT
class DiffInput(BaseModel):
    operation: str = "unused"
    options: DiffOptions

class IntInput(BaseModel):
    operation: str = "unused"
    options: IntOptions

class OptimInput(BaseModel):
    operation: str = "unused"
    options: OptimOptions

class LagrangeInput(BaseModel):
    operation: str = "unused"
    options: LagrangeOptions

class TaylorInput(BaseModel):
    operation: str = "unused"
    options: TaylorOptions
