class DuplicateIPv4Error(Exception):
    pass


class LabNotFoundError(Exception):
    pass


class PodNotFoundError(Exception):
    pass


class PodAlreadyExists(Exception):
    pass

class LabAlreadyExistsError(Exception):
    pass