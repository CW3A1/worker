import database, time

def openfoam(pc, task_id):
    database.busyScheduler(pc)
    time.sleep(10)
    database.freeScheduler(pc)