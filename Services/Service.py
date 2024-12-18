from Repositories.DBRepository import EmployeeRepository
from DtoModels.EmployeeDto import EmployeeDto
from models.EmployeeInfo import EmployeeInfo
from Interfaces.IService import IService


class Mapper:
    @staticmethod
    def conver_to_dto(data: EmployeeInfo) -> EmployeeDto:
        return EmployeeDto(**data.model_dump())

    @staticmethod
    def convert_from_dto(self, data: EmployeeDto) -> EmployeeInfo:
        return EmployeeInfo(**data.model_dump())


class Service(IService):
    def __init__(self):
        self.repos_emp = EmployeeRepository()

    def add(self, data: EmployeeDto) -> None:
        employee = EmployeeInfo(**data.model_dump())
        self.repos_emp.insert(employee)

    def get(self) -> list[EmployeeDto]:
        repos_data = self.repos_emp.select()
        result = list(map(Mapper.conver_to_dto, repos_data))
        return result

    def update(self, data: EmployeeDto) -> None:
        employee = EmployeeInfo(**data.model_dump())
        self.repos_emp.update(employee)

    def delete(self, id: int) -> None:
        self.repos_emp.delete(id)



