from pydantic import BaseModel

class EmployeeDto(BaseModel):
    name: str
    surname: str
    patronymic: str