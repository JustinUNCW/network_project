from fastapi import APIRouter, Depends
from app.models.pod_model import *
from app.services.pod_store import PodDB
from app.dependencies.dependencies import get_pod_db


router = APIRouter(
    prefix="/labs/{lab_id}"
    
)

@router.get("/pods/{pod_id}", tags=["Pod"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> PodExists:
    '''Get a pod within a lab'''
    return pod_db.get_pod_by_id(lab_id, pod_id)
     
@router.get("/pods/{pod_id}/network", tags=["Pod", "Network"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> IPv4Network:
    '''Get a pods network'''
    return pod_db.get_pod_network(lab_id, pod_id)
     

@router.get("/pods/{pod_id}/addresses/used", tags=["Pod", "Address"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> dict:
    '''Get all IPv4 addresses used within a pod'''
    return {'addresses': pod_db.get_all_pod_ip(lab_id, pod_id)}
    

@router.get("/pods/{pod_id}/addresses/free", tags=["Pod", "Address"])
async def get_pod_addresses_free(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> dict:
    '''Get all free IP's within the pods network'''
    return {'addresses': pod_db.get_free_pod_ip(lab_id, pod_id)}
     
    
@router.post("/pods", response_model=PodExists, tags=["Pod"])
async def create_pod(lab_id: str, 
                     pod: PodCreate, 
                     pod_db: PodDB = Depends(get_pod_db)
                     ) -> PodExists:
    '''Create a pod within a lab'''
    return pod_db.create_pod(lab_id, pod)
     

@router.delete("/pods/{pod_id}/delete", tags=["Pod"])
async def delete_pod(
    lab_id: str, 
    pod_id: str, 
    pod_db: PodDB = Depends(get_pod_db)
    ) -> dict:
    '''delete a pod'''
    pod_db.delete_pod(lab_id, pod_id)
    return {"detail": f"Pod {pod_id} has been deleted"}
