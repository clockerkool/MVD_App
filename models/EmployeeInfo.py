from pydantic import BaseModel

class EmployeeInfo(BaseModel, extra='forbid'):
    id: int | None
    name: str
    surname: str
    patronymic: str