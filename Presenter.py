import logging

from DtoModels.EmployeeDto import EmployeeDto
from Services.Service import Service
from Interfaces.IService import IService

class Mapper:
    @staticmethod
    def conver_to_dto(data: dict) -> EmployeeDto:
        return EmployeeDto(**data)


class Presenter:
    def __init__(self, service: IService):
        self.service = service

    def add_employee(self, data: dict) -> None:
        data = Mapper.conver_to_dto(data)
        self.service.add(data)

    def get_all_employees(self) -> list:
        result = self.service.get()
        logging.info("Presenter: Returned all employees.")
        return result

    def update_employee(self, data: dict) -> None:
        data = Mapper.conver_to_dto(data)
        self.service.update(data)
        logging.info("Presenter: Employee updated successfully.")

    def delete_employee(self, id: int) -> None:
        self.service.delete(id)
        logging.info("Presenter: Employee deleted successfully.")


presenter = Presenter(Service())
