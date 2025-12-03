from fastapi import FastAPI
from app.routers import lab_pod_router, upload_router

app = FastAPI()

app.include_router(upload_router.router)
app.include_router(lab_pod_router.router)
