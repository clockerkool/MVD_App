import sqlite3 as sq
from models.EmployeeInfo import EmployeeInfo
from models.InsertEmployeeData import InsertEmployeeData


class DatabaseConnection:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = sq.connect("Kurse.db")
        self.conn.row_factory = sq.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class BaseRepository:
    def __init__(self, connection):
        self.connection = connection


class EmployeeRepository(BaseRepository):
    def insert(self, employee_data: InsertEmployeeData) -> None:
        query = """INSERT INTO employee (name, surname, patronymic) VALUES (?, ?, ?)"""

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (employee_data.name, employee_data.surname, employee_data.patronymic))
            conn.commit()

    def select(self) -> list[EmployeeInfo]:
        query = """select * from employee"""

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        return [EmployeeInfo(**row) for row in rows]

    def update(self, employee_data: EmployeeInfo) -> None:
        query = """UPDATE employee SET name = ?, surname = ?, patronymic = ? WHERE id = ?"""

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (employee_data.name, employee_data.surname, employee_data.patronymic, employee_data.id))
            conn.commit()

    def delete(self, employee_id: int) -> None:
        query = """DELETE FROM employee WHERE id = ?"""

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (employee_id,))
            conn.commit()

