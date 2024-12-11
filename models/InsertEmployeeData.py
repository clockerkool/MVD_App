from pydantic import BaseModel

class InsertEmployeeData(BaseModel, extra='forbid'):
    name: str
    surname: str
    patronymic: str