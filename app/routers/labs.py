from fastapi import APIRouter, Depends
from app.models.lab_db_model import LabMeta 
from app.services.lab_store import LabDB
from app.services.pod_store import PodDB
from app.main import get_lab_db, get_pod_db

router = APIRouter(
    prefix="/lab",
    tags=["Lab"],
)

@router.get("/{lab_id}", response_model=LabMeta)
async def get_lab_meta(
    lab_id: str,
    lab_db: LabDB = Depends(get_lab_db),
) -> LabMeta:
    """Get a Lab by id"""
    return lab_db.get_lab_meta(lab_id)

@router.put("/{lab_id}/replace")
async def update_lab_meta(
    lab_id: str,
    lab: LabMeta,
    lab_db: LabDB = Depends(get_lab_db),
) -> dict:
    """Replace the lab's data (excluding pods)"""
    lab_db.put_lab_meta(lab_id, lab)  # <-- use put, not get
    return {"detail": f"Lab {lab_id} has been updated"}

@router.post("/{lab_id}/create")
async def create_lab_meta(
    lab_id: str,
    lab: LabMeta,
    lab_db: LabDB = Depends(get_lab_db),
    lab_pod_db: PodDB = Depends(get_pod_db),
) -> dict:
    lab_db.create_new_lab_meta(lab_id, lab)
    lab_pod_db._init_lab_pods(lab_id)
    return {"detail": f"Lab {lab_id} has been created"}

@router.delete("/{lab_id}/delete")
async def delete_lab_and_lab_meta(
    lab_id: str, 
    lab_db: LabDB = Depends(get_lab_db),
    lab_pod_db: PodDB = Depends(get_pod_db)
    ) -> dict:
    lab_db.delete_lab_meta(lab_id)
    lab_pod_db.delete_lab_and_pod(lab_id)
    return {"detail": f"Lab {lab_id} and it's pods have been deleted"}