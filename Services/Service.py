from Repositories.DBRepository import EmployeeRepository
from DtoModels.EmployeeDto import EmployeeDto
from models.EmployeeInfo import EmployeeInfo
from Interfaces.IService import IService
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Service(IService):
    def __init__(self):
        self.repos_emp = EmployeeRepository()
        self.logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler('../service.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def add(self, data: dict) -> None:
        employee = EmployeeInfo(**data)
        self.repos_emp.insert(employee)
        logging.info("Service: Added new employee")

    def get(self) -> list[EmployeeInfo]:
        data = self.repos_emp.select()
        logging.info(f"Service: Selected all employee: {data}")
        return data

    def update(self, data: dict) -> None:
        employee = EmployeeInfo(**data)
        self.repos_emp.update(employee)
        logging.info(f"Service: Updated employee with id={EmployeeInfo.id}")

    def delete(self, id: int) -> None:
        self.repos_emp.delete(id)
        logging.info(f"Service: Deleted employee with id={EmployeeInfo.id}")

print(Service().get())

