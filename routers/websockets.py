from asyncio import sleep

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from modules import database, environment
from orjson import dumps as jsondumps

router = APIRouter()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pc = await websocket.receive_text()
    init_data = database.status_scheduler(pc).dict()
    await websocket.send_text(jsondumps(init_data).decode("utf-8"))
    while (act_data:=database.status_scheduler(pc).dict()) == init_data:
        await sleep(1.5)
    await websocket.send_text(jsondumps(act_data).decode("utf-8"))

@router.get("/test")
async def get():
    return HTMLResponse(f"""
                        <body>
                        </body>
                        <script>
                            var ws = new WebSocket("{environment.WS_URL}");
                            ws.onmessage = function(event) {{
                                console.log(JSON.parse(event.data))
                                document.body.innerHTML = JSON.parse(event.data)["pc"] + "|" + JSON.parse(event.data)["status"]
                            }};
                            ws.onopen = () => ws.send("eeklo");
                            window.onbeforeunload = function() {{
                                ws.onclose = function () {{}};
                                ws.close();
                            }};
                        </script>
                        """)
