from fastapi import APIRouter
from modules import database
from pydantic import BaseModel

router = APIRouter()

class SchedulerInfo(BaseModel):
    pc: str
    status: int

@router.get("/api/scheduler/status/{pc}", response_model=SchedulerInfo, tags=["schedulers"])
def view_scheduler_status(pc: str):
    return database.status_scheduler(pc)

@router.get("/api/scheduler/free/{pc}", response_model=SchedulerInfo, tags=["schedulers"])
def free_scheduler(pc: str):
    database.free_scheduler(pc)
    return database.status_scheduler(pc)

@router.get("/api/scheduler/busy/{pc}", response_model=SchedulerInfo, tags=["schedulers"])
def busy_scheduler(pc: str):
    database.busy_scheduler(pc)
    return database.status_scheduler(pc)