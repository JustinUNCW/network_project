from fastapi import File, UploadFile, HTTPException, APIRouter, Depends, Response, status
from app.models.lab_model import *
from app.models.lab_db_model import *
from app.models.pod_model import *
from app.services.lab_store import LabDB
from app.services.pod_store import PodDB
from app.dependencies.dependencies import get_pod_db, get_lab_db
import json

router = APIRouter(
    prefix="/upload", 
    tags=["Bulk"]
)

@router.post("/bulk", status_code=201)
async def upload_pod_dump(
    file: UploadFile = File(),
    lab_db: LabDB = Depends(get_lab_db),
    pod_db: PodDB = Depends(get_pod_db),
) -> LabExistsDump:
    """Bulk upload multiple labs and pods"""

    resp = LabExistsDump()

    if file.content_type not in ("application/json", "text/json"):
        raise HTTPException(status_code=400, detail="File must be JSON")

    raw = await file.read()

    try:
        req = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    lab_dump = LabCreateDump.model_validate(req)

    for lab in lab_dump.data: 
        lab_meta_exists = lab_db.create_new_lab_meta(
            LabMetaCreate(
                name=lab.name, 
                location=lab.location, 
                building=lab.building, 
                floor=lab.floor), pod_db)
        
        pod_exists = []

        for pod in lab.pods:
            pod_exists.append(pod_db.create_pod(lab_meta_exists.id, pod))

        resp.data.append(
                LabExists(
                    **lab_meta_exists.model_dump(),
                    pods=pod_exists
                )
        )

    return resp
