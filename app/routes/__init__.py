import time
import anyio.to_thread
from fastapi import APIRouter

router_app = APIRouter()

def tarea_sincrona_pesada():
    time.sleep(5)
    return "Resultado de tarea síncrona"


@router_app.get("/example")
async def endpoint_asincrono():

    resultado = await anyio.to_thread.run_sync(tarea_sincrona_pesada)

    return {"resultado": resultado}
