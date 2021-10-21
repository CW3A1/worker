import json
import threading
import time

import numpy

import database


def openfoam_thread(data_points, pc, task_id):
    data_pointsx = data_points[:4]
    data_pointsy = data_points[4:]
    A = numpy.array([[int(x)**3, int(x)**2, int(x)**1, 1] for x in data_pointsx])
    b = numpy.array([[int(y)] for y in data_pointsy])
    res = [arr[0] for arr in numpy.linalg.solve(A,b).tolist()]
    time.sleep(15)
    database.complete_task(task_id, res)
    database.free_scheduler(pc)

def next_openfoam_thread():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        database.pending_task(oldestPendingTask, randomFreeScheduler)
        database.busy_scheduler(randomFreeScheduler)
        of_thread = threading.Thread(target = openfoam_thread, args = (json.loads(database.status_task(oldestPendingTask)[oldestPendingTask]['input_values']), randomFreeScheduler, oldestPendingTask))
        of_thread.start()
