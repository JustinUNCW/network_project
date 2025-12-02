from fastapi import FastAPI
from app.routers import uploads, pods

app = FastAPI()

app.include_router(uploads.router)
app.include_router(pods.router)
