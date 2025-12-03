from pydantic import BaseModel
from app.models.pod_model import Pod

class Lab(BaseModel):
    id: str
    name: str
    location: str
    building: str
    floor: str
    pods: list[Pod]