from typing import Dict, List

from pydantic import BaseModel


# OPTIONS
class DiffOptions(BaseModel):
    task_id: str = ""
    f: str = "sin(x)"
    a: float = 0
    order: int = 1

class IntOptions(BaseModel):
    task_id: str = ""
    f: str = "sin(x)"
    a: float = -1
    b: float = 1

class OptimOptions(BaseModel):
    task_id: str = ""
    f: str = "sin(x)"
    xl: float = -1
    xu: float = 1
    yl: float = -1
    yu: float = 1

class LagrangeOptions(BaseModel):
    task_id: str = ""
    a: List[float]
    b: List[float]

class TaylorOptions(BaseModel):
    task_id: str = ""
    f: str = "sin(x)"
    x0: float = 0
    order: int = 1

class HeatOptions(BaseModel):
    task_id: str = ""
    L_X: float = 5
    L_Y: float = 5
    H: float = 0.3
    ALPHA: float = 10**6
    T: float = 5
    FPS: int = 15
    BOUNDARY_CONDITION: str = "NO_FLUX"