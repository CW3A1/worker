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
def new_task(task_input: classes.DiffInput):
    return differentiate.numDiff(task_input.options.f, task_input.options.a, task_input.options.order)

@app.post("/num_math/integration")
def new_task(task_input: classes.IntInput):
    return integrate.numInt(task_input.options.f, gen.Inf if task_input.options.a=="Inf" else (-gen.Inf if task_input.options.a=="-Inf" else task_input.options.a), gen.Inf if task_input.options.b=="Inf" else (-gen.Inf if task_input.options.b=="-Inf" else task_input.options.b))

@app.post("/num_math/optimization")
def new_task(task_input: classes.OptimInput):
    return optimize.twoDNumOpt(task_input.options.f, task_input.options.xl, task_input.options.xu, task_input.options.yl, task_input.options.yu)

@app.post("/num_math/lagrange_interpolation")
def new_task(task_input: classes.LagrangeInput):
    return lagrange.lagrangePoly(task_input.options.a, task_input.options.b)

@app.post("/num_math/taylor_approximation")
def new_task(task_input: classes.TaylorInput):
    return taylor.approximateTaylorPoly(task_input.options.f, task_input.options.x0, task_input.options.order)

@app.post("/num_math/heat_equation")
def new_task(task_input: classes.HeatInput):
    return heat_equation.calcAnimUp(task_input.options)
