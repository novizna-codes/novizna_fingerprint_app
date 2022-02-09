import sys
import os
from pathlib import Path

BASE_DIRECTORY=Path(__file__).parent

sys.path.append(str(BASE_DIRECTORY.joinpath("dlls").absolute()))
os.add_dll_directory(str(BASE_DIRECTORY.joinpath("dlls").absolute()))

from typing import Optional, List, Dict, Any
from multiprocessing import Process

import uvicorn
from PyQt5.QtWidgets import QApplication
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseSettings, Field, BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect
from tortoise import manager
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.exceptions import DoesNotExist
import mimetypes
import random
from models import FingerPrintModel
from ui import MainWindow, TrayIcon, UiProcess
from zk import FingerPrint


mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/svg+xml', '.svg')

window=None
window_callback=None
class Settings (BaseSettings):
    zk:FingerPrint = Field(default_factory=lambda : FingerPrint())
    connected_device:int=-1
    is_connected:bool=False
    window:Any=None
    test_mode:bool=True

class WebSocketManager:

    def __init__(self, *args, **kwargs):
        self.active_connections:List[WebSocket]=[]

    async def connect(self,websocket:WebSocket,connection_id=None):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self,websocket:WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self,message:Dict,websocket:WebSocket):
        await websocket.send_json(message)


    async def broadcast(self,message:Dict):
        for connection in self.active_connections:
            await connection.send_json(message)


socket_manager=WebSocketManager()



app = FastAPI()

settings=Settings()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FingerPrintMatchRequest(BaseModel):
    name:str
    template:str
    status:int

app.mount("/data", StaticFiles(directory="data/"), name="data")
app.mount("/assets", StaticFiles(directory="data/assets/"), name="assets")
templates = Jinja2Templates(directory="data")


@app.on_event('startup')
async def on_startup() -> None:
    if settings.test_mode:
        return
    FingerPrint.init_db()
    FingerPrint.re_init()


@app.on_event('shutdown')
async def on_shutdown() -> None:
    if settings.test_mode:
        return
    FingerPrint.close_db()
    settings.zk.close_device()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/settings")
def app_settings():
    return {
        "device":settings.connected_device,
        "connected":settings.is_connected
    }

@app.get("/devices")
async def devices():
    if settings.test_mode:
        return {
            "success": True,
            "devices": 2
        }
    FingerPrint.re_init()
    devices=settings.zk.available_devices()
    if devices>0:
        return {
            "success":True,
            "devices": devices
        }
    else:
        return {
            "success": False,
            "message":"Unable to connect to device",
            "devices": devices
        }

@app.get("/connect/{id}")
async def connect(id:int):
    if settings.test_mode:
        if id<2:
            settings.connected_device = id
            settings.is_connected = True
            return {"success": True}
        else:
            return {
                "success": False,
                "message": "Unable to connect"
            }
    try:
        settings.zk.open_device(id)
        settings.connected_device=id
        settings.is_connected=True
        return {"success":True}
    except Exception as e:
        raise e
        return HTTPException(status_code=400, detail={
            "success":False,
            "message":e
        })

@app.post("/disconnect")
async def disconnect():
    if settings.test_mode:
        settings.is_connected = False
        settings.connected_device = -1
        return {"success": True}
    try:
        settings.zk.close_device()
        settings.is_connected=False
        settings.connected_device=-1
        return {"success":True}
    except Exception as e:
        return HTTPException(status_code=400, detail={
            "success":False,
            "message":e
        })

@app.get("/save/{name}")
async def save_template(name:str):
    try:
        instance=await FingerPrintModel.get(name=name)
    except DoesNotExist as e:
        instance=FingerPrintModel()
        instance.name=name
    await socket_manager.broadcast({
        "type": "START_FINGERPRINT_SCAN"
    })
    template = settings.zk.get_finger_print()

    if template:
        instance.template=template
        await socket_manager.broadcast({
            "type": "SAVED_FINGERPRINT_SCAN"
        })
        await instance.save()
        return {
            "success":True,

        }
    else:
        return {
            "success":False,
        }

@app.post("/match")
async def match_fingerprint(data:FingerPrintMatchRequest):
    finger_template=data.template
    if settings.test_mode:
        status=data.status
        await socket_manager.broadcast({
            "type": "START_FINGERPRINT_SCAN"
        })
        result=0
        if status==0:
            result=random.randint(0,49)
        else:
            result=random.randint(50,100)
        await socket_manager.broadcast({
            "type": "FINISH_FINGERPRINT_SCAN",
            "result": result
        })
        return {
            "success": True,
            "match": result
        }
    instance=await FingerPrintModel.get(name=data.name)
    saved_template=instance.template
    if settings.zk.is_connected():
        await socket_manager.broadcast({
            "type": "START_FINGERPRINT_SCAN"
        })
        current_template=settings.zk.get_finger_print()
        result=FingerPrint.match_finger_templates(template_1=current_template,template_2=saved_template)
        await socket_manager.broadcast({
            "type": "FINISH_FINGERPRINT_SCAN",
            "result":result
        })
        return {
            "success":True,
            "match":result
        }
    else:
        return HTTPException(
            status_code=400,
            detail={
                "success":False,
                "message":"Device not connected"
            }

        )

@app.websocket("/socket")
async def sockets(websocket:WebSocket):
    await socket_manager.connect(websocket)
    try:
        while True:
            data=await websocket.receive_json()
            print(data)
            await socket_manager.broadcast({"Hello":"Received"})
    except WebSocketDisconnect:
        await socket_manager.disconnect(websocket)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)



def start_ui(settings):
    settings=settings['settings']
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.resize(400, 600)
    settings.window=window
    trayIcon = TrayIcon(app, window)
    app.exec_()

if __name__ == '__main__':
    # process=Process(target=start_ui,args=({"settings":settings},))
    process=UiProcess()
    process.start()
    uvicorn.run(app)