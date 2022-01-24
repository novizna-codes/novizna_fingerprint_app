from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseSettings, Field, BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.exceptions import DoesNotExist

from models import FingerPrintModel
from zk import FingerPrint

class Settings (BaseSettings):
    zk:FingerPrint = Field(default_factory=lambda : FingerPrint())
app = FastAPI()

settings=Settings()


class FingerPrintMatchRequest(BaseModel):
    name:str
    template:str


@app.on_event('startup')
async def on_startup() -> None:
    FingerPrint.init_db()
    settings.zk.open_device(0)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    FingerPrint.close_db()
    settings.zk.close_device()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/devices")
async def read_item():
    devices=settings.zk.available_devices()
    print(f"found devices {devices}")
    return {"devices": devices}

@app.get("/connect/{id}")
async def read_item(id:int):
    try:
        settings.zk.open_device(id)
        return {"success":True}
    except Exception as e:
        raise e
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