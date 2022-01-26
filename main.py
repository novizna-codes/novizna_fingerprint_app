from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseSettings, Field, BaseModel
from starlette.responses import RedirectResponse
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.exceptions import DoesNotExist

from models import FingerPrintModel
from zk import FingerPrint

class Settings (BaseSettings):
    zk:FingerPrint = Field(default_factory=lambda : FingerPrint())
    connected_device:int=-1
    is_connected:bool=False

app = FastAPI()

settings=Settings()

origins = [
    "http://localhost:3000",
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


@app.on_event('startup')
async def on_startup() -> None:
    pass
    FingerPrint.init_db()
    FingerPrint.re_init()
    # settings.zk.open_device(0)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    pass
    FingerPrint.close_db()
    # settings.zk.close_device()

@app.get("/")
async def home():
    response = RedirectResponse(url='http://localhost:3000/#/')
    return response

@app.get("/settings")
def app_settings():
    return {
        "device":settings.connected_device,
        "connected":settings.is_connected
    }

@app.get("/devices")
async def devices():
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
    template = settings.zk.get_finger_print()

    if template:
        instance.template=template
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
    instance=await FingerPrintModel.get(name=data.name)
    saved_template=instance.template
    if settings.zk.is_connected():
        current_template=settings.zk.get_finger_print()
        result=FingerPrint.match_finger_templates(template_1=current_template,template_2=saved_template)
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


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)