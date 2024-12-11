import logging


class Presenter:
    def __init__(self, service):
        self.service = service

    def add_employee(self, data: dict) -> None:
        try:
            self.service.add_employee(data)
            logging.info("Presenter: Employee added successfully.")
        except Exception as e:
            logging.error(f"Presenter: Error adding employee - {e}")

    def get_all_employees(self) -> list:
        try:
            employees = self.service.get_all_employees()
            logging.info("Presenter: Retrieved all employees.")
            return employees
        except Exception as e:
            logging.error(f"Presenter: Error retrieving employees - {e}")
            return []

    def update_employee(self, data: dict) -> None:
        try:
            self.service.update_employee(data)
            logging.info("Presenter: Employee updated successfully.")
        except Exception as e:
            logging.error(f"Presenter: Error updating employee - {e}")

    def delete_employee(self, id: int) -> None:
        try:
            self.service.delete_employee(id)
            logging.info("Presenter: Employee deleted successfully.")
        except Exception as e:
            logging.error(f"Presenter: Error deleting employee - {e}")