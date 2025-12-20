from typing import Optional
from fastapi import APIRouter, Depends
from app.models.pod_model import *
from app.services.pod_store import PodDB
from app.dependencies.dependencies import get_pod_db


router = APIRouter(
    prefix="/lab/{lab_id}/pods/{pod_id}", 
)

@router.get("/devices", tags=["Device"])
async def get_pod_devices(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> dict[str, list[DeviceExists]]:
    '''Get all pod devices'''
    devices = pod_db.get_pod_devices(lab_id, pod_id)
    return {'devices': devices}

@router.post("/device", tags=["Device"])
async def create_device(lab_id: str, 
                        pod_id: str, 
                        device: DeviceCreate, 
                        pod_db: PodDB = Depends(get_pod_db)
                        ) -> DeviceExists:
    '''Create a device within a pod'''
    return pod_db.create_device(lab_id, pod_id, device)
     

@router.patch("/device/{device_id}/ip", tags=["Device", "Network"])
async def update_device_ip(lab_id: str, 
                           pod_id: str, 
                           device_id: str, 
                           ip: str,  
                           pod_db: PodDB = Depends(get_pod_db)
                           ) -> dict[str, DeviceExists]:
    '''Update a devices IPv4 address'''
    device = pod_db.patch_device_ip(lab_id, pod_id, device_id, ip)
    return {"device": device}

@router.patch("/device{device_id}/name", tags=["Device"])
async def update_device_name(lab_id: str, 
                             pod_id: str, 
                             device_id: str, 
                             name: str, pod_db: PodDB = Depends(get_pod_db)
                             ) -> dict[str, DeviceExists]:
    '''Update a devices name'''
    device = pod_db.patch_device_name(lab_id, pod_id, device_id, name)
    return {"device": device}

@router.patch("/device/{device_id}/accessMethod", tags=["Device", "Access Methodss"])
async def update_device_accessMethod(lab_id: str, 
                                     pod_id: str, 
                                     device_id: str, 
                                     access: AccessMethod, 
                                     pod_db: PodDB = Depends(get_pod_db)
                                     ) -> dict[str, DeviceExists]:
    '''Update a devices access method'''
    device = pod_db.patch_device_access_method(lab_id, pod_id, device_id, access)
    return {"device": device}

@router.patch("/device/network", tags=["Device", "Network"])
async def udpate_device_network(lab_id: str, 
                                pod_id: str, 
                                device_id: str, 
                                network: Network, 
                                pod_db: PodDB = Depends(get_pod_db)
                                ) -> dict[str, list[DeviceExists]]:
    '''Update all pod devices network'''
    devices = pod_db.patch_pod_devices_network(lab_id, pod_id, device_id, network)
    return {"devices": devices}

@router.patch("/device/location", tags=["Device", "Location"])
async def update_device_location(lab_id: str, 
                                 pod_id: str, 
                                 location: Location, 
                                 pod_db: PodDB = Depends(get_pod_db)
                                 ) -> dict[str, list[DeviceExists]]:
    '''Update all pod devices location'''
    device = pod_db.patch_pod_devices_location(lab_id, pod_id, location)
    return {"device": device}

@router.delete("/device/{device_id}/delete", tags=['Device'])
async def delete_device(lab_id: str, 
pod_id: str, 
device_id: str, 
pod_db: PodDB = Depends(get_pod_db)
) -> dict[str, str]: 
    pod_db.delete_device(lab_id, pod_id, device_id)
    return {"detail": f'Device {device_id} has been deleted'}