from typing import Optional
from fastapi import APIRouter, Depends
from app.models.pod_model import Device, Location, Network, AccessMethod
from app.services.pod_store import PodDB
from app.main import get_pod_db


router = APIRouter(
    prefix="/lab/{lab_id}/pods/{pod_id}", 
)

@router.get("/devices", tags=["Device"])
async def get_pod_devices(lab_id: str, 
                  pod_id: str, 
                  pod_db: PodDB = Depends(get_pod_db)
                  ) -> list[Device]:
    '''Get all pod devices'''
    devices = pod_db.get_pod_devices(lab_id, pod_id)
    return devices

@router.post("/device", tags=["Device"])
async def create_device(lab_id: str, 
                        pod_id: str, 
                        device: Device, 
                        pod_db: PodDB = Depends(get_pod_db)
                        ) -> dict:
    '''Create a device within a pod'''
    pod_db.create_device(lab_id, pod_id, device)
    return {"detail": "Device successfully created"}

@router.patch("/device/{device_id}/ip", tags=["Device"])
async def update_device_ip(lab_id: str, 
                           pod_id: str, 
                           device_id: str, 
                           ip: str,  pod_db: PodDB = Depends(get_pod_db)
                           ) -> dict:
    '''Update a devices IPv4 address'''
    pod_db.patch_device_ip(lab_id, pod_id, device_id, ip)
    return {"detail": f"Device {device_id} IPv4 address updated"}

@router.patch("/device{device_id}/name", tags=["Device"])
async def update_device_name(lab_id: str, 
                             pod_id: str, 
                             device_id: str, 
                             name: str, pod_db: PodDB = Depends(get_pod_db)
                             ) -> dict:
    '''Update a devices name'''
    pod_db.patch_device_name(lab_id, pod_id, device_id, name)
    return {"detail": f"Device {device_id} name has been updated"}

@router.patch("/device/{device_id}/accessMethod", tags=["Device"])
async def update_device_accessMethod(lab_id: str, 
                                     pod_id: str, 
                                     device_id: str, 
                                     access: AccessMethod, 
                                     pod_db: PodDB = Depends(get_pod_db)
                                     ) -> dict:
    '''Update a devices access method'''
    pod_db.patch_device_access_method(lab_id, pod_id, device_id, access)
    return {"detail": f"Device {device_id} access method has been updated"}

@router.patch("/device/{device_id}/network", tags=["Device"])
async def udpate_device_network(lab_id: str, 
                                pod_id: str, 
                                device_id: str, 
                                network: Network, 
                                pod_db: PodDB = Depends(get_pod_db)
                                ) -> dict:
    '''Update a devices network'''
    pod_db.patch_pod_devices_network(lab_id, pod_id, device_id, network)
    return {"detail": f"Device {device_id} netowrk has been updated"}

@router.patch("/device/location", tags=["Device"])
async def update_device_location(lab_id: str, 
                                 pod_id: str, 
                                 location: Location, 
                                 pod_db: PodDB = Depends(get_pod_db)
                                 ) -> dict:
    '''Update all pod devices location'''
    pod_db.patch_pod_devices_location(lab_id, pod_id, location)
    return {"detail": f"Devices location has been updated"}

@router.delete("/device/{device_id}/delete")
async def delete_device(lab_id: str, 
pod_id: str, 
device_id: str, 
pod_db: PodDB = Depends(get_pod_db)
) -> dict: 
    pod_db.delete_device(lab_id, pod_id, device_id)
    return {"detail": f'Device {device_id} has been deleted'}