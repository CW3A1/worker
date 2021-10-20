import database, openfoam, threading

def runNext():
    randomFreeScheduler = database.randomFreeScheduler()
    oldestPendingTask = database.oldestPendingTask()
    if randomFreeScheduler:
        if oldestPendingTask:
            openfoam_thread = threading.Thread(target=openfoam.openfoam, name="OpenFoam", args=(randomFreeScheduler, oldestPendingTask))
            openfoam_thread.start()
            return {randomFreeScheduler:oldestPendingTask}
        return {'error': 'no tasks to run'}
    return {'error': 'no pc available'}