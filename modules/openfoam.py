import numpy

from modules import database


def openfoam_thread(data_points, pc, task_id):
    data_pointsx = data_points[:4]
    data_pointsy = data_points[4:]
    A = numpy.array([[x**3, x**2, x**1, 1] for x in data_pointsx])
    b = numpy.array([[y] for y in data_pointsy])
    res = [round(arr[0], 3) for arr in numpy.linalg.solve(A,b).tolist()]
    database.complete_task(task_id, res)
    database.change_scheduler_status(pc, 0)

def next_openfoam_thread():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        database.pending_task(oldestPendingTask, randomFreeScheduler)
        database.change_scheduler_status(randomFreeScheduler, 1)
        openfoam_thread(database.status_task(oldestPendingTask)['input_values'], randomFreeScheduler, oldestPendingTask)
