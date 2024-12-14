import sqlite3 as sq

from Interfaces.IRepository import IRepository
from models.EmployeeInfo import EmployeeInfo
from DtoModels.EmployeeDto import EmployeeDto
import logging

logging.basicConfig(filename='../service.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseConnection:
    def __init__(self):
        self.conn = sq.connect("Kurse.db")
        self.conn.row_factory = sq.Row

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class EmployeeRepository(IRepository):
    def insert(self, employee_data: EmployeeInfo) -> None:
        query = """INSERT INTO employee (name, surname, patronymic) VALUES (?, ?, ?)"""
        print(employee_data)
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (employee_data.name, employee_data.surname, employee_data.patronymic))
            conn.commit()

    def select(self) -> list[EmployeeInfo]:
        query = """select * from employee"""

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [EmployeeInfo(**row) for row in rows]

    def update(self, employee_data: EmployeeInfo) -> None:
        query = """UPDATE employee SET name = ?, surname = ?, patronymic = ? WHERE id = ?"""

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (employee_data.name, employee_data.surname, employee_data.patronymic, employee_data.id))
            conn.commit()

    def delete(self, employee_id: int) -> None:
        try:
            query = """DELETE FROM employee WHERE id = ?"""
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (employee_id,))
                conn.commit()

        except Exception as e:
            print(f"Error in delete: {e}")

