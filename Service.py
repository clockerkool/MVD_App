from DBRepository import BaseRepository, EmployeeRepository
from models.InsertEmployeeData import InsertEmployeeData
from models.EmployeeInfo import EmployeeInfo
import logging

logging.basicConfig(filename='service.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Service:
    def __init__(self):
        self.repos_emp = EmployeeRepository()

    def add_employee(self, data: dict) -> None:
        employee = InsertEmployeeData(**data)
        self.repos_emp.insert(employee)
        logging.info("Added new employee")

    def get_all_employees(self) -> list[EmployeeInfo]:
        data = self.repos_emp.select()
        logging.info(f"Selected all employee: {data}")

        return data

    def update_employee(self, data: dict) -> None:
        employee = EmployeeInfo(**data)
        self.repos_emp.update(employee)
        logging.info(f"Updated employee with id={EmployeeInfo.id}")

    def delete_employee(self, id: int) -> None:
        self.repos_emp.delete(id)
        logging.info(f"Deleted employee with id={EmployeeInfo.id}")



service = Service()
service.get_all_employees()