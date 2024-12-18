from abc import ABC, abstractmethod
from models.EmployeeInfo import EmployeeInfo

class IRepository(ABC):
    @abstractmethod
    def insert(self, employee_data: EmployeeInfo) -> None:
        pass

    @abstractmethod
    def select(self) -> list[EmployeeInfo]:
        pass

    @abstractmethod
    def update(self, employee_data: EmployeeInfo) -> None:
        pass

    @abstractmethod
    def delete(self, employee_id: int) -> None:
        pass