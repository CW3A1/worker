from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from modules import (classes, differentiate, heat_equation, integrate,
                     lagrange, optimize, taylor)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

@app.post("/num_math/differentiation")
def new_task(task_input: classes.DiffOptions, background: BackgroundTasks):
    background.add_task(differentiate.numDiff, task_id=task_input.task_id, f=task_input.f, a=task_input.a, o=task_input.order)
    return {"response": "OK"}

@app.post("/num_math/integration")
def new_task(task_input: classes.IntOptions, background: BackgroundTasks):
    background.add_task(integrate.numInt, task_id=task_input.task_id, f=task_input.f, a=task_input.a, b=task_input.b)
    return {"response": "OK"}

@app.post("/num_math/optimization")
def new_task(task_input: classes.OptimOptions, background: BackgroundTasks):
    background.add_task(optimize.twoDNumOpt, task_id=task_input.task_id, f=task_input.f, x_l=task_input.xl, x_u=task_input.xu, y_l=task_input.yl, y_u=task_input.yu)
    return {"response": "OK"}

@app.post("/num_math/lagrange_interpolation")
def new_task(task_input: classes.LagrangeOptions, background: BackgroundTasks):
    background.add_task(lagrange.lagrangePoly, task_id=task_input.task_id, a=task_input.a, b=task_input.b)
    return {"response": "OK"}

@app.post("/num_math/taylor_approximation")
def new_task(task_input: classes.TaylorOptions, background: BackgroundTasks):
    background.add_task(taylor.approximateTaylorPoly, task_id=task_input.task_id, f=task_input.f, x0=task_input.x0, degree=task_input.order)
    return {"response": "OK"}

@app.post("/num_math/heat_equation")
def new_task(task_input: classes.HeatOptions, background: BackgroundTasks):
    background.add_task(heat_equation.calcAnimUp, task_id=task_input.task_id, heat_options=task_input)
    return {"response": "OK"}
