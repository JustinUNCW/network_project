from ipaddress import IPv4Address, IPv4Network
from pydantic import BaseModel

class Network(BaseModel):
    network: IPv4Network
    gateway: IPv4Address

class Interface(BaseModel):
    address: IPv4Address
    parent: Network

class Port(BaseModel):
    interface: Interface

class Location(BaseModel):
    row: str
    aisle: str

class AccessMethod(BaseModel):
    url: str

class Device(BaseModel):
    id: str
    name: str
    description: str
    accessMethods: list[AccessMethod]
    location: Location
    ports: list[Port]

class Pod(BaseModel):
    '''
    - Models a Pod
    - id: 1010
    - assets: One Device or multiple Devices 
    '''
    id: str
    assets: list[Device]