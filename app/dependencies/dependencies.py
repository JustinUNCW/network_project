from app.services.pod_store import *
from app.services.lab_store import LabDB

pod_db = PodDB()
lab_db = LabDB()

def get_pod_db():
    return pod_db

def get_lab_db():
    return lab_db