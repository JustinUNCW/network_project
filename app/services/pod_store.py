from typing import Dict
from app.models.pod_model import Pod

# simple in-memory store: pod_id -> Pod
pods_by_id: Dict[str, Pod] = {}
