import uuid
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from modules import auth, database, openfoam
from pydantic import BaseModel

router = APIRouter()

class TaskInput(BaseModel):
    p1: List[float]
    p2: List[float]
    p3: List[float]
    p4: List[float]

class TaskOutput(BaseModel):
    id: str
    status: str
    pc: str
    input_values: List[float]
    result: List[float]
    uuid: str

@router.post("/api/task/add", response_model=TaskOutput, tags=["tasks"])
async def add_task(task_data: TaskInput, background: BackgroundTasks, identifier: str = Depends(auth.header_to_identifier)):
    task_id = str(uuid.uuid4())[:8]
    r = [task_data.p1[0], task_data.p2[0], task_data.p3[0], task_data.p4[0], task_data.p1[1], task_data.p2[1], task_data.p3[1], task_data.p4[1]]
    resp = database.add_task(task_id, r, identifier)
    background.add_task(openfoam.next_openfoam_thread)
    return resp

@router.get("/api/task/status/{task_id}", response_model=TaskOutput, tags=["tasks"])
async def view_task_status(task_id: str, identifier: str = Depends(auth.header_to_identifier)):
    if (resp := database.status_task(task_id)):
        if resp["uuid"] in {"", identifier}:
            return resp
        raise HTTPException(status_code=403)
    raise HTTPException(status_code=404)
