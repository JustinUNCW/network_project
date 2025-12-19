from fastapi import APIRouter, Depends
from app.models.lab_db_model import * 
from app.services.lab_store import LabDB
from app.services.pod_store import PodDB
from app.dependencies.dependencies import get_pod_db, get_lab_db

router = APIRouter(
    prefix="/labs",
    tags=["Lab"]
)

@router.get("/{lab_id}")
async def get_lab_meta(
    lab_id: str,
    lab_db: LabDB = Depends(get_lab_db)
) -> dict[str, LabMetaExists]:
    """Get a Lab by id"""
    lab = lab_db.get_lab_meta(lab_id)
    return {'lab': LabMetaExists(id=lab_id, **lab.model_dump())}

@router.put("/{lab_id}/replace",  status_code=201)
async def update_lab_meta(
    lab_id: str,
    lab: LabMetaCreate,
    lab_db: LabDB = Depends(get_lab_db),
) -> dict[str, LabMetaExists]:
    """Replace the lab's data (excluding pods)"""
    lab = lab_db.put_lab_meta(lab_id, lab)  
    return {"lab": lab}

@router.post("/create", status_code=201)
async def create_lab_meta(
    lab: LabMetaCreate,
    lab_db: LabDB = Depends(get_lab_db),
    lab_pod_db: PodDB = Depends(get_pod_db),
) -> LabMetaExists:
    return lab_db.create_new_lab_meta(lab, lab_pod_db)

@router.delete("/{lab_id}/delete")
async def delete_lab_and_lab_meta(
    lab_id: str, 
    lab_db: LabDB = Depends(get_lab_db),
    lab_pod_db: PodDB = Depends(get_pod_db)
    ) -> dict:
    lab_db.delete_lab_meta(lab_id)
    lab_pod_db.delete_lab_and_pod(lab_id)
    return {"detail": f"Lab {lab_id} and it's pods have been deleted"}