from fastapi import HTTPException, APIRouter
from app.services.pod_store import pods_by_id


router = APIRouter(
    prefix="/pod", 
    tags=["Pod"]
)


@router.get("/{pod_id}")
def get_pod(pod_id: str):

    pod = pods_by_id.get(pod_id)

    if pod is None:
        raise HTTPException(status_code=404, detail="Pod not found")

    return pod 
