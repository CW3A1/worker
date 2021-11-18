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

class HeatOptions(BaseModel):
    L_X: float = 5
    L_Y: float = 5
    H: float = 0.3
    ALPHA: float = 10**6
    T: float = 5
    FPS: int = 15
    BOUNDARY_CONDITION: str = "NO_FLUX"

# INPUT
class DiffInput(BaseModel):
    operation: str = "diff"
    options: DiffOptions

class IntInput(BaseModel):
    operation: str = "int"
    options: IntOptions

class OptimInput(BaseModel):
    operation: str = "opt"
    options: OptimOptions

class LagrangeInput(BaseModel):
    operation: str = "lint"
    options: LagrangeOptions

class TaylorInput(BaseModel):
    operation: str = "taprox"
    options: TaylorOptions

class HeatInput(BaseModel):
    operation: str = "heateq"
    options: HeatOptions