from typing import Dict
from app.models.lab_db_model import LabMeta

# simple in-memory store: lab_id -> Lab
labs_by_id: Dict[str, LabMeta] = {}
