from abc import ABC, abstractmethod
from models.EmployeeInfo import EmployeeInfo

class IService(ABC):
    @abstractmethod
    def add(self, data: dict) -> None:
        pass

    @abstractmethod
    def get(self) -> list[EmployeeInfo]:
        pass

    @abstractmethod
    def update(self, data: dict) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass