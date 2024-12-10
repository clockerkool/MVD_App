import sqlite3 as sq
from utils import get_db_path

class DatabaseConnection:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = sq.connect("Kurse.db")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class BaseRepository:
    def __init__(self, connection):
        self.connection = connection


class EmployeeRepository(BaseRepository):
    def insert(self, employee_data: list) -> None:
        query = """insert into employee"""

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, employee_data)
            conn.commit()

    def select(self):
        query = """select * from employee"""

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchall()
            return row

repos = EmployeeRepository(DatabaseConnection())
print(repos.select())
