from pydantic import BaseModel
from pydantic.types import StringConstraints
from typing_extensions import Annotated

NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1)
]

class LabMetaCreate(BaseModel):
    name: NonEmptyStr
    location: NonEmptyStr
    building: NonEmptyStr
    floor: NonEmptyStr

class LabMetaExists(BaseModel):
    id: NonEmptyStr
    name: NonEmptyStr
    location: NonEmptyStr
    building: NonEmptyStr
    floor: NonEmptyStr