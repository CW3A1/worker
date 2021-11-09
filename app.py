from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

from modules import differentiate, integrate, lagrange, optimize, taylor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pno3cwa1.student.cs.kuleuven.be",
        "http://localhost:5000",
        "http://localhost:11000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

class TaskInput(BaseModel):
    operation: str
    options: Dict

@app.post("/new_task")
def new_task(task_input: TaskInput):
    if task_input.operation == "diff":
        return differentiate.numDiff(task_input.options["f"], task_input.options["a"], task_input.options["order"] if "order" in task_input.options else 1)
    if task_input.operation == "int":
        return integrate.numInt(task_input.options["f"], task_input.options["a"], task_input.options["b"])
    if task_input.operation == "optimize":
        return optimize.twoDNumOpt(task_input.options["f"], task_input.options["xl"], task_input.options["xu"], task_input.options["yl"], task_input.options["yu"])
    if task_input.operation == "lagrangeInterpolation":
        return lagrange.lagrangePoly(task_input.options["a"], task_input.options["b"])
    if task_input.operation == "taylorApproximation":
        return taylor.approximateTaylorPoly(task_input.options["f"], task_input.options["x0"], task_input.options["order"])