from typing import Optional
from fastapi import APIRouter, Depends
from app.models.pod_model import Pod, Device, Location, Network, IPv4Address
from app.services.pod_store import PodDB
from app.main import get_pod_db


router = APIRouter(
    prefix="/lab/{lab_id}",
)

@router.get("/pods/{pod_id}", tags=["Pod"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> Optional[Pod]:
    '''Get a pod within a lab'''
    pod = pod_db.get_pod_by_id(lab_id, pod_id)
    return pod

@router.get("/pods/{pod_id}/location", tags=["Pod", "Location"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> Optional[Location]:
    '''Get a pods location'''
    location = pod_db.get_pod_location(lab_id, pod_id)
    return location

@router.get("/pods/{pod_id}/network", tags=["Pod", "Network"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> Optional[Network]:
    '''Get a pods network'''
    network = pod_db.get_pod_network(lab_id, pod_id)
    return network

@router.get("/pods/{pod_id}/addresses/used", tags=["Pod", "Address"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> Optional[list[IPv4Address]]:
    '''Get all IPv4 addresses used within a pod'''
    addr = pod_db.get_all_pod_ip(lab_id, pod_id)
    return addr

@router.get("/pods/{pod_id}/addresses/free", tags=["Pod", "Address"])
async def get_pod(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> Optional[Device]:
    '''Get all pod devices'''
    pod = pod_db.get_pod_devices(lab_id, pod_id)
    return pod
    
@router.post("/pods", tags=["Pod"])
async def create_pod(lab_id: str, 
                     pod: Pod, 
                     pod_db: PodDB = Depends(get_pod_db)
                     ) -> dict:
    '''Create a pod within a lab'''
    pod_db(lab_id, pod)
    return {"message": f"Pod {pod.id} successfully created"}

@router.put("/pods/{pod_id}/replace", tags=["Pod"])
async def put_pod(
    lab_id: str, 
    pod: Pod, 
    pod_db: PodDB = Depends(get_pod_db)
    ) -> dict:
    '''Replace a pod'''
    pod_db.put_pod(lab_id, pod)
    return {"message": f"Pod {pod.id} successfully replaced"}

@router.delete("/pods/{pod_id}/delete", tags=["Pod"])
async def delete_pod(
    lab_id: str, 
    pod_id: str, 
    pod_db: PodDB = Depends(get_pod_db)
    ) -> dict:
    '''delete a pod'''
    pod_db.delete_pod(lab_id, pod_id)
    return {"detail": f"Pod {pod_id} has been deleted"}
