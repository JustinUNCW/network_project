from typing import Dict
from app.models.lab_db_model import *
from app.Exceptions.exceptions import LabNotFoundError, LabAlreadyExistsError
from app.services.pod_store import PodDB

class LabDB: 
    def __init__(self):
        self.labs_by_id: Dict[str, LabMetaCreate] = {}

    def get_lab_meta(self, lab_id: str) -> LabMetaExists: 
        lab = self.labs_by_id.get(lab_id)

        if lab is not None: 
            return LabMetaExists(id=lab_id, **lab.model_dump())
        
        raise LabNotFoundError(f'Lab {lab_id} does not exist')
    
    def put_lab_meta(self, lab_id: str, lab: LabMetaExists) -> LabMetaExists:

        try: 
            self.labs_by_id[lab_id] = lab
            return LabMetaExists(id=lab_id, **lab.model_dump())
        
        except KeyError:
            raise LabNotFoundError(f'Lab {lab_id} does not exist')
    
    def create_new_lab_meta(self, lab: LabMetaCreate, lab_pods: PodDB) -> LabMetaExists:
        
        lab_id = lab_pods._init_lab()

        self.labs_by_id[lab_id] = lab

        return LabMetaExists(id=lab_id, **lab.model_dump())
 
    def delete_lab_meta(self, lab_id) -> bool:
        if lab_id not in self.labs_by_id:
            raise LabNotFoundError(f'Lab {lab_id} does not exist')
        del self.labs_by_id[lab_id]
        return True
