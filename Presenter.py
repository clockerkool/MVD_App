import logging
from DtoModels.EmployeeDto import EmployeeDto
from Services.Service import Service
from models.EmployeeInfo import EmployeeInfo


class Mapper:
    def conver_to_dto(self, data: dict | EmployeeInfo) -> EmployeeDto:
        return EmployeeDto(**data) if type(data) == dict else EmployeeDto(**data.model_dump())

    def convert_from_dto(self, data: EmployeeDto) -> EmployeeInfo:
        return EmployeeInfo(**data.model_dump())


class Presenter:
    def __init__(self, service):
        self.service = service
        self.mapper = Mapper()

    def add_employee(self, data: dict) -> None:
        try:
            data = self.mapper.conver_to_dto(data)
            self.service.add_employee(data)
            logging.info("Presenter: Employee added successfully.")
        except Exception as e:
            logging.error(f"Presenter: Error - {e}")

    def get_all_employees(self) -> list:
        # try:
        employees = self.service.get()
        logging.info("Presenter: Returned all employees.")
        result = list(map(self.mapper.conver_to_dto, employees))
        return result

        # except Exception as e:
        #     logging.error(f"Presenter: Error - {e}")
        #     return []

    def update_employee(self, data: dict) -> None:
        try:
            data = self.mapper.conver_to_dto(data)
            self.service.update_employee(data)
            logging.info("Presenter: Employee updated successfully.")
        except Exception as e:
            logging.error(f"Presenter: Error - {e}")

    def delete_employee(self, id: int) -> None:
        try:
            self.service.delete_employee(id)
            logging.info("Presenter: Employee deleted successfully.")
        except Exception as e:
            logging.error(f"Presenter: Error - {e}")

