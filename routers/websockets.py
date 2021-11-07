from random import randint
from time import sleep

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    while True:
        sleep(1)
        await websocket.send_text(f"randomnumber: {randint(1,10)}")

@router.get("/test")
async def get():
    return HTMLResponse("""
                        <body>
                        </body>
                        <script>
                            var ws = new WebSocket("ws://localhost:11001/ws");
                            ws.onmessage = function(event) {
                                console.log(event.data)
                                document.body.innerHTML = event.data
                            };
                            ws.onopen = () => ws.send("");
                        </script>
                        """)