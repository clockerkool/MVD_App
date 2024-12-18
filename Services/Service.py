from Repositories.DBRepository import EmployeeRepository
from DtoModels.EmployeeDto import EmployeeDto
from models.EmployeeInfo import EmployeeInfo
from Interfaces.IService import IService
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Service(IService):
    def __init__(self):
        self.repos_emp = EmployeeRepository()

    def add(self, data: EmployeeDto) -> None:
        employee = EmployeeInfo(**data.model_dump())
        self.repos_emp.insert(employee)

    def get(self) -> list[EmployeeInfo]:
        data = self.repos_emp.select()
        return data

    def update(self, data: EmployeeDto) -> None:
        employee = EmployeeInfo(**data.model_dump())
        self.repos_emp.update(employee)

    def delete(self, id: int) -> None:
        self.repos_emp.delete(id)



