from fastapi import File, UploadFile, HTTPException, APIRouter
from app.models.lab_model import Lab
from app.models.lab_db_model import LabMeta
from app.services.pod_store import pods_by_id
from app.services.lab_store import labs_by_id
import json

router = APIRouter(
    prefix="/upload", 
    tags=["Uploads"]
)

@router.post("/dump")
async def upload_pod_dump(file: UploadFile = File()):
    if file.content_type not in ("application/json", "text/json"):
        raise HTTPException(status_code=400, detail="File must be JSON")

    raw = await file.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    lab = Lab.model_validate(data)

    labs_by_id[lab.id] = LabMeta(
        id=lab.id, 
        name=lab.name, 
        location=lab.location,
        building=lab.building, 
        floor=lab.floor)

    pods_by_id[lab.id] = {}

    for pod in lab.pods:
        pods_by_id[lab.id][pod.id] = pod

    return {"Pods uploaded": len(lab.pods)}