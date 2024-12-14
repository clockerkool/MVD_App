from pydantic import BaseModel

class EmployeeDto(BaseModel):
    id: int | None = None
    name: str
    surname: str
    patronymic: str