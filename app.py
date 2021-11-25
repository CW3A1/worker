from multiprocessing import Pool, set_start_method

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from modules import classes, heat_equation, num_math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

try:
    pool = Pool(processes=4)
    set_start_method('spawn')
except RuntimeError:
    pass

@app.post("/num_math/differentiation")
async def new_task(task_input: classes.DiffOptions):
    res = pool.apply_async(num_math.numDiff, (task_input.task_id, task_input.f, task_input.a, task_input.order))
    res.get(timeout=20)
    return {"response": "OK"}

@app.post("/num_math/integration")
async def new_task(task_input: classes.IntOptions):
    res = pool.apply_async(num_math.numInt, (task_input.task_id, task_input.f, task_input.a, task_input.b))
    res.get(timeout=20)
    return {"response": "OK"}

@app.post("/num_math/optimization")
async def new_task(task_input: classes.OptimOptions):
    res = pool.apply_async(num_math.twoDNumOpt, (task_input.task_id, task_input.f, task_input.xl, task_input.xu, task_input.yl, task_input.yu))
    res.get(timeout=20)
    return {"response": "OK"}

@app.post("/num_math/lagrange_interpolation")
async def new_task(task_input: classes.LagrangeOptions):
    res = pool.apply_async(num_math.lagrangePoly, (task_input.task_id, task_input.a, task_input.b))
    res.get(timeout=20)
    return {"response": "OK"}

@app.post("/num_math/taylor_approximation")
async def new_task(task_input: classes.TaylorOptions):
    res = pool.apply_async(num_math.approximateTaylorPoly, (task_input.task_id, task_input.f, task_input.x0, task_input.order))
    res.get(timeout=20)
    return {"response": "OK"}

@app.post("/num_math/heat_equation")
async def new_task(task_input: classes.HeatOptions):
    res = pool.apply_async(heat_equation.calcAnimUp, (task_input.task_id, task_input))
    res.get(timeout=120)
    return {"response": "OK"}
