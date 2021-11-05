from fastapi import APIRouter, HTTPException
from modules import database, environment
from pydantic import BaseModel

router = APIRouter()

class SchedulerInfo(BaseModel):
    pc: str = "brugge"
    status: int = 0

@router.put("/status", response_model=SchedulerInfo, tags=["schedulers"])
def change_scheduler_status(new_info: SchedulerInfo, auth: str):
    if auth == environment.AUTH_SECRET:
        if database.scheduler_exists(new_info.pc):
            if new_info.status in (0, 1, 2):
                database.change_scheduler_status(new_info.pc, new_info.status)
                return database.status_scheduler(new_info.pc)
            raise HTTPException(status_code=403)
        raise HTTPException(status_code=404)
    raise HTTPException(status_code=401)

@router.get("/status/{pc}", response_model=SchedulerInfo, tags=["schedulers"])
def view_scheduler_status(pc: str):
    if database.scheduler_exists(pc):
        return database.status_scheduler(pc)
    raise HTTPException(status_code=404)
