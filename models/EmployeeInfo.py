from pydantic import BaseModel

class EmployeeInfo(BaseModel, extra='forbid'):
    id: int
    name: str
    surname: str
    patronymic: str