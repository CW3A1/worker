import json
import threading
import time

import numpy

import database


def openfoam_thread(data_points, pc, task_id):
    A = numpy.array([[int(data_points[x][0])**3, int(data_points[x][0])**2, int(data_points[x][0])**1, 1] for x in data_points])
    b = numpy.array([[int(data_points[x][1])] for x in data_points])
    res = "/".join([str(arr[0]) for arr in numpy.linalg.solve(A,b).tolist()])
    time.sleep(15)
    database.complete_task(task_id, res)
    database.free_scheduler(pc)

def next_openfoam_thread():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        database.pending_task(oldestPendingTask, randomFreeScheduler)
        database.busy_scheduler(randomFreeScheduler)
        of_thread = threading.Thread(target = openfoam_thread, args = (json.loads(database.status_task(oldestPendingTask)[oldestPendingTask]['input_values'].replace("1", "\"1\"").replace("2", "\"2\"").replace("3", "\"3\"").replace("4", "\"4\"")), randomFreeScheduler, oldestPendingTask))
        of_thread.start()
