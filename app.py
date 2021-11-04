from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import schedulers, tasks, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pno3cwa1.student.cs.kuleuven.be",
        "http://localhost:5000",
        "http://localhost:11000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schedulers.router)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
