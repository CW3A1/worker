import uuid
from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from modules import auth, database, openfoam
from pydantic import BaseModel

router = APIRouter()

class TaskInput(BaseModel):
    p1: List[float] = [0, 0]
    p2: List[float] = [0, 0]
    p3: List[float] = [0, 0]
    p4: List[float] = [0, 0]

class TaskOutput(BaseModel):
    task_id: str
    status: str = 0
    pc: str
    input_values: List[float] = [0, 0, 0, 0, 0, 0, 0, 0]
    result: List[float] = [0, 0, 0, 0]
    uuid: str

class TaskList(BaseModel):
    tasks: List[TaskOutput]
    uuid: str

@router.post("/add", response_model=TaskOutput, tags=["tasks"])
async def add_task(task_data: TaskInput, background: BackgroundTasks, identifier: str = Depends(auth.header_to_identifier)):
    task_id = str(uuid.uuid4())[:8]
    r = [task_data.p1[0], task_data.p2[0], task_data.p3[0], task_data.p4[0], task_data.p1[1], task_data.p2[1], task_data.p3[1], task_data.p4[1]]
    database.add_task(task_id, r, identifier)
    background.add_task(openfoam.next_openfoam_thread)
    return database.status_task(task_id)

@router.get("/status", response_model=TaskOutput, tags=["tasks"])
async def view_task_status(task_id: str, identifier: str = Depends(auth.header_to_identifier)):
    if database.task_exists(task_id):
        resp = database.status_task(task_id)
        if resp["uuid"] in {"", identifier}:
            return resp
        raise HTTPException(status_code=403)
    raise HTTPException(status_code=404)
