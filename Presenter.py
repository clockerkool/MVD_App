import logging

from PyQt5.QtWidgets import QMessageBox

from DtoModels.EmployeeDto import EmployeeDto
from Services.Service import Service
from Interfaces.IService import IService
from models.EmployeeInfo import EmployeeInfo


class Mapper:
    def conver_to_dto(self, data: dict | EmployeeInfo) -> EmployeeDto:
        return EmployeeDto(**data) if type(data) == dict else EmployeeDto(**data.model_dump())

    def convert_from_dto(self, data: EmployeeDto) -> EmployeeInfo:
        return EmployeeInfo(**data.model_dump())


class Presenter:
    def __init__(self, service: IService):
        self.service = service
        self.mapper = Mapper()

    def add_employee(self, data: dict) -> None:
        data = self.mapper.conver_to_dto(data)
        self.service.add(data)

    def search(self) -> list:
        employees = self.service.get()
        logging.info("Presenter: Returned all employees.")
        result = list(map(self.mapper.conver_to_dto, employees))
        return result

    def update_employee(self, data: dict) -> None:
        data = self.mapper.conver_to_dto(data)
        self.service.update(data)
        logging.info("Presenter: Employee updated successfully.")

    def delete_employee(self, id: int) -> None:
        self.service.delete(id)
        logging.info("Presenter: Employee deleted successfully.")


presenter = Presenter(Service())
