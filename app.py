from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from modules import (classes, differentiate, gen, heat_equation, integrate,
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
def new_task(task_input: classes.DiffOptions):
    return differentiate.numDiff(task_input.f, task_input.a, task_input.order)

@app.post("/num_math/integration")
def new_task(task_input: classes.IntOptions):
    return integrate.numInt(task_input.f, gen.Inf if task_input.a=="Inf" else (-gen.Inf if task_input.a=="-Inf" else task_input.a), gen.Inf if task_input.b=="Inf" else (-gen.Inf if task_input.b=="-Inf" else task_input.b))

@app.post("/num_math/optimization")
def new_task(task_input: classes.OptimOptions):
    return optimize.twoDNumOpt(task_input.f, task_input.xl, task_input.xu, task_input.yl, task_input.yu)

@app.post("/num_math/lagrange_interpolation")
def new_task(task_input: classes.LagrangeOptions):
    return lagrange.lagrangePoly(task_input.a, task_input.b)

@app.post("/num_math/taylor_approximation")
def new_task(task_input: classes.TaylorOptions):
    return taylor.approximateTaylorPoly(task_input.f, task_input.x0, task_input.order)

@app.post("/num_math/heat_equation")
def new_task(task_input: classes.HeatOptions):
    return heat_equation.calcAnimUp(task_input)
