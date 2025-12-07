from typing import Dict
from app.models.lab_db_model import LabMeta
from app.Exceptions.exceptions import LabNotFoundError, LabAlreadyExistsError

class LabDB: 
    def __init__(self):
        self.labs_by_id: Dict[str, LabMeta] = {}

    def get_lab_meta(self, lab_id: str) -> LabMeta: 
        meta = self.labs_by_id.get(lab_id)
        if meta is not None: 
            return meta
        raise LabNotFoundError(f'Lab {lab_id} does not exist')
    
    def put_lab_meta(self, lab_id: str, lab: LabMeta) -> bool:
        if lab_id not in self.labs_by_id:
            raise LabNotFoundError(f'Lab {lab_id} does not exist')

        self.labs_by_id[lab_id] = lab
        return True
    
    def create_new_lab_meta(self, lab_id: str, lab: LabMeta) -> bool:
        if lab_id in self.labs_by_id:
            raise LabAlreadyExistsError(f'Lab {lab_id} already exists')

        self.labs_by_id[lab_id] = lab
        return True
    
    def delete_lab_meta(self, lab_id) -> bool:
        if lab_id not in self.labs_by_id:
            raise LabNotFoundError(f'Lab {lab_id} does not exist')
        del self.labs_by_id[lab_id]
        return True
