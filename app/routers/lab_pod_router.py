from fastapi import HTTPException, APIRouter
from app.models.pod_model import Pod
from app.services.pod_store import pods_by_id
from app.services.lab_store import labs_by_id, LabMeta


router = APIRouter(
    prefix="/lab", 
)

@router.get("/{lab_id}", tags=["Lab"])
async def get_lab(lab_id: str) -> LabMeta: 
    '''Get a Lab by id'''

    lab = labs_by_id.get(lab_id)

    if lab is None: 
        raise HTTPException(status_code=404, detail=f"Lab {lab_id} not found")
    return lab


@router.get("/{lab_id}/pods/{pod_id}", tags=["Pod"])
async def get_pod(lab_id: str, pod_id: str) -> Pod:
    '''Get a pod within a lab'''

    lab = pods_by_id.get(lab_id)
    if lab is None:
        raise HTTPException(status_code=404, detail=f"Lab {lab_id} not found")
    
    pod = lab.get(pod_id)

    if pod is None: 
        raise HTTPException(status_code=404, detail=f"Pod {pod_id} not found")
    return pod 

@router.post("/{lab_id}/pods", tags=["Pod"])
async def upload_pod(lab_id: str, pod: Pod):
    '''Upload a pod to a lab'''

    pods_by_id[lab_id][pod.id] = pod
    return {"Total number of pods": len(pods_by_id[lab_id])}

