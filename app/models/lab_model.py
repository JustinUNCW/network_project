from typing import Optional
from pydantic import BaseModel, Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated
from app.models.pod_model import PodExists, PodCreate

NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1)
]


class LabCreate(BaseModel):
    name: NonEmptyStr
    location: NonEmptyStr
    building: NonEmptyStr
    floor: NonEmptyStr
    pods: list[PodCreate]

class LabExists(BaseModel):
    id: NonEmptyStr
    name: NonEmptyStr
    location: NonEmptyStr
    building: NonEmptyStr
    floor: NonEmptyStr
    pods: list[PodExists]

class LabExistsDump(BaseModel):
    data: Optional[list[LabExists]] =  Field(default_factory=list)

class LabCreateDump(BaseModel):
    data: Optional[list[LabCreate]] =  Field(default_factory=list)