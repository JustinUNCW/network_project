from ipaddress import IPv4Address, IPv4Network
from pydantic import BaseModel
from pydantic.types import StringConstraints
from typing_extensions import Annotated

NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1)
]

class Network(BaseModel):
    network: IPv4Network
    gateway: IPv4Address

class Interface(BaseModel):
    address: IPv4Address
    parent: Network

class Port(BaseModel):
    interface: Interface

class Location(BaseModel):
    row: NonEmptyStr
    aisle: NonEmptyStr

class AccessMethod(BaseModel):
    url: str

class DeviceCreate(BaseModel):
    name: NonEmptyStr
    description: NonEmptyStr
    accessMethods: list[AccessMethod]
    location: Location
    ports: list[Port]

class DeviceExists(BaseModel):
    id: NonEmptyStr
    name: NonEmptyStr
    description: NonEmptyStr
    accessMethods: list[AccessMethod]
    location: Location
    ports: list[Port]


class PodCreate(BaseModel):
    '''
    - Models a Pod
    - assets: One Device or multiple Devices 
    '''
    assets: list[DeviceCreate]

class PodExists(BaseModel):
    id: NonEmptyStr
    assets: list[DeviceExists]