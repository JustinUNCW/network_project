# app/services/pod_store.py
from typing import Dict
from app.models.models import Pod

# simple in-memory store: pod_id -> Pod
pods_by_id: Dict[str, Pod] = {}
