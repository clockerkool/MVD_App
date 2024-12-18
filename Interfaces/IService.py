from abc import ABC, abstractmethod

from DtoModels.EmployeeDto import EmployeeDto
from models.EmployeeInfo import EmployeeInfo

class IService(ABC):
    @abstractmethod
    def add(self, data: dict) -> None:
        pass

    @abstractmethod
    def get(self) -> list[EmployeeDto]:
        pass

    @abstractmethod
    def update(self, data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass