from fastapi import File, UploadFile, HTTPException, APIRouter
from app.models.models import Pod
from app.services.pod_store import pods_by_id
import json


router = APIRouter(
    prefix="/upload", 
    tags=["Uploads"]
)


class PodTrack():
    def __init__(self):
        self.pods = []
        self.len = 0

track = PodTrack()

@router.post("/dump")
async def upload_pod_dump(file: UploadFile = File()):
    if file.content_type not in ("application/json", "text/json"):
        error = HTTPException(status_code=400, detail="File must be JSON")
        return error.detail

    raw = await file.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    for wrapper in data:
        for pod_data in wrapper.get("data", []):
            pod = Pod.model_validate(pod_data)
            pods_by_id[pod.id] = pod
            track.len += 1

    return {"Pods uploaded": track.len}


@router.post("/pod")
async def upload_pod(pod: Pod):
    pods_by_id[pod.id] = pod
    track.len += 1

    return {"Total number of pods": track.len}