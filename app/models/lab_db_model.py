from pydantic import BaseModel

class LabMeta(BaseModel):
    id: str
    name: str
    location: str
    building: str
    floor: str