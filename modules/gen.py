from os import remove
from time import time_ns

import numpy
from requests import post
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from sympy import Poly, init_printing
from sympy.abc import *
from sympy.parsing.sympy_parser import (convert_xor,
                                        implicit_multiplication_application,
                                        parse_expr, standard_transformations)
from sympy.utilities.lambdify import lambdify

from modules.environment import DB_URL

init_printing(use_unicode=True)

def parseString(f: str):
    parse_string = parse_expr(f, transformations=standard_transformations+(convert_xor, implicit_multiplication_application,))
    return parse_string

def evalString(f: str, free_vars: set = set()):
    parse_string = parseString(f)
    if len(free_vars) > 0:
        f = lambdify(list(free_vars), parse_string, "numpy")
    else:
        f = lambdify(list(parse_string.free_symbols), parse_string, "numpy")
    return f

def oneDPolyToStr(f: numpy.poly1d):
    return str(Poly([round(num, 5) for num in f.coef], x).as_expr())

def postToDB(task_id: str, res):
    post(f"{DB_URL}/api/task/complete", json={"task_id": task_id, "data": res})

def uploadToUguu(filename):
    file_host_url = "https://uguu.se/api.php?d=upload-tool"
    file = open(filename, "rb")
    data = {'file': (file.name, file, "image/gif")}
    encoder = MultipartEncoder(fields=data)
    monitor = MultipartEncoderMonitor(encoder)
    r = post(file_host_url, data=monitor, headers={'Content-Type': monitor.content_type})
    r = r.text
    file.close()
    remove(filename)
    return r

def add_log(text):
    post(f"{DB_URL}/api/logs/add", json={"unix_time": time_ns(), "text": text})