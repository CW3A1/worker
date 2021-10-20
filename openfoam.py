import threading
import time

import database


def openfoam_thread(pc, task_id):
    time.sleep(15)
    database.free_scheduler(pc)
    database.complete_task(task_id)

def next_openfoam_thread():
    randomFreeScheduler = database.random_free_scheduler()
    oldestPendingTask = database.oldest_pending_task()
    if randomFreeScheduler:
        if oldestPendingTask:
            database.busy_scheduler(randomFreeScheduler)
            of_thread = threading.Thread(target = openfoam_thread, name = "OpenFoam", args = (randomFreeScheduler, oldestPendingTask))
            of_thread.start()
