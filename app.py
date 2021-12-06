from multiprocessing import Pool, set_start_method

from flask import Flask
from flask_pydantic import validate

from modules import classes, heat_equation, num_math

app = Flask(__name__)

@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response

try:
    pool = Pool(processes=4)
    set_start_method('spawn')
except RuntimeError:
    pass

@app.route("/num_math/differentiation", methods=["POST"])
@validate()
def numDiff_(body: classes.DiffOptions):
    res = pool.apply_async(num_math.numDiff, (body.task_id, body.f, body.a, body.order))
    try:
        res.get(timeout=1)
    except:
        pass
    return "OK"

@app.route("/num_math/integration", methods=["POST"])
@validate()
async def numInt_(body: classes.IntOptions):
    res = pool.apply_async(num_math.numInt, (body.task_id, body.f, body.a, body.b))
    try:
        res.get(timeout=1)
    except:
        pass
    return "OK"

@app.route("/num_math/optimization", methods=["POST"])
@validate()
async def twoDNumOpt_(body: classes.OptimOptions):
    res = pool.apply_async(num_math.twoDNumOpt, (body.task_id, body.f, body.xl, body.xu, body.yl, body.yu))
    try:
        res.get(timeout=1)
    except:
        pass
    return "OK"

@app.route("/num_math/lagrange_interpolation", methods=["POST"])
@validate()
async def lagrangePoly_(body: classes.LagrangeOptions):
    res = pool.apply_async(num_math.lagrangePoly, (body.task_id, body.a, body.b))
    try:
        res.get(timeout=1)
    except:
        pass
    return "OK"

@app.route("/num_math/taylor_approximation", methods=["POST"])
@validate()
async def approximateTaylorPoly_(body: classes.TaylorOptions):
    res = pool.apply_async(num_math.approximateTaylorPoly, (body.task_id, body.f, body.x0, body.order))
    try:
        res.get(timeout=1)
    except:
        pass
    return "OK"

@app.route("/num_math/heat_equation", methods=["POST"])
@validate()
async def calcAnimUp_(body: classes.HeatOptions):
    res = pool.apply_async(heat_equation.calcAnimUp, (body.task_id, body))
    try:
        res.get(timeout=1)
    except:
        pass
    return "OK"

if __name__ == "__main__":
    app.run()