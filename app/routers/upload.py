from fastapi import File, UploadFile, HTTPException, APIRouter, Depends
from app.models.lab_model import Lab
from app.models.lab_db_model import LabMeta
from app.services.lab_store import LabDB
from app.services.pod_store import PodDB
from app.main import get_lab_db, get_pod_db
import json

router = APIRouter(
    prefix="/upload", 
    tags=["Bulk"]
)

@router.post("/bulk")
async def upload_pod_dump(
    file: UploadFile = File(),
    lab_db: LabDB = Depends(get_lab_db),
    pod_db: PodDB = Depends(get_pod_db),
) -> dict:
    """Bulk upload multiple labs and pods"""

    if file.content_type not in ("application/json", "text/json"):
        raise HTTPException(status_code=400, detail="File must be JSON")

    raw = await file.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    lab = Lab.model_validate(data)

    lab_db.create_new_lab_meta(
        lab.id,
        LabMeta(
            id=lab.id,
            name=lab.name,
            location=lab.location,
            building=lab.building,
            floor=lab.floor,
        ),
    )

    pod_db._init_lab_pods(lab.id)

    for pod in lab.pods:
        pod_db.create_pod(lab.id, pod)

    return {"detail": f"Lab {lab.id} and its pods have been created"}
