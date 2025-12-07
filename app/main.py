from fastapi import FastAPI
from app.routers import pods, devices, labs, upload
from app.services.pod_store import *
from app.services.lab_store import LabDB
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse



app = FastAPI()
pod_db = PodDB()
lab_db = LabDB()

def get_pod_db():
    return pod_db

def get_lab_db():
    return lab_db

@app.exception_handler(LabNotFoundError)
async def lab_not_found_handler(request: Request, exc: LabNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc) or "Lab not found"},
    )

@app.exception_handler(PodNotFoundError)
async def pod_not_found_handler(request: Request, exc: PodNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc) or "Pod not found"},
    )

@app.exception_handler(PodAlreadyExists)
async def pod_exists_handler(request: Request, exc: PodAlreadyExists):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc) or "Pod already exists"},
    )

@app.exception_handler(DuplicateIPv4Error)
async def duplicate_ip_handler(request: Request, exc: DuplicateIPv4Error):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc) or "Duplicate IPv4 addresses not allowed"},
    )


app.include_router(router=pods.router)
app.include_router(router=devices.router)
app.include_router(router=labs.router)
app.include_router(router=upload.router)
