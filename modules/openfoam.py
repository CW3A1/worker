from numpy import polyfit

from modules import database


def openfoam_thread(data_points, pc, task_id):
    x = data_points[:4]
    y = data_points[4:]
    res = [round(num, 3) for num in polyfit(x, y, 3)]
    database.complete_task(task_id, res)
    database.change_scheduler_status(pc, 0)

def next_openfoam_thread():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler and oldestPendingTask:
        database.pending_task(oldestPendingTask, randomFreeScheduler)
        database.change_scheduler_status(randomFreeScheduler, 1)
        openfoam_thread(database.status_task(oldestPendingTask)["input_values"], randomFreeScheduler, oldestPendingTask)
