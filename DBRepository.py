import pyodbc

from DB_functions import get_id_sysb
from utils import get_db_path

class DatabaseConnection:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.db_path + ';'
        )
        self.conn = pyodbc.connect(conn_str)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class BaseRepository:
    def __init__(self, connection):
        self.connection = connection

class EmployeeRepository(BaseRepository):
    def insert(self, employee_data: list) -> None:
        query = """insert into Сотрудники (Фамилия, Имя, Отчество, ДатаРождения, Пол, Должность, Звание, Подразделение, Регион, Телефон, СНИЛС) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, employee_data)
            conn.commit()

    def update(self, id, employee_data):
        with self.connection as conn:
            cursor = conn.cursor()
            sql = """UPDATE Сотрудники SET ... WHERE Кодсотрудника = ?"""
            cursor.execute(sql, employee_data + (id,))  # Объединение данных
            conn.commit()

class CabinetRepository(BaseRepository):
    def insert(self, data: list) -> None:
        query = """insert into Кабинеты (Номер, Улица, Дом) values (?, ?, ?)"""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()


class OSRepository(BaseRepository):
    def insert(self, data: list) -> None:
        query = """insert into ОперационныеСистемы (Наименование, КодСистемногоБлока) values (?, ?)"""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()

class SysUnitRepository(BaseRepository):
    def insert(self, data: list) -> None:
        query = """insert into СистемныеБлоки (Модель, ИнвентарныйНомер, IP, ВиртуальныйIP, Кодкабинета, Кодсотрудника) values (?, ?, ?, ?, ?, ?)"""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()

class TechDevicesRepository(BaseRepository):
    def insert(self, container: list[list]) -> None:
        sysb_id = get_id_sysb()
        with self.connection as conn:
            cursor = conn.cursor()
            for name, mark, sys_num in container:
                cursor.execute(
                    "insert into ТехническиеСредства (Наименование, Марка, СерийныйНомер, КодСистемногоБлока) values (?, ?, ?, ?)",
                    name, mark, sys_num, sysb_id)
            conn.commit()

class UnitOfWork:
    def __init__(self, db_path):
        self.connection = DatabaseConnection(db_path)
        self.employees = EmployeeRepository(self.connection)
        self.cabinets = CabinetRepository(self.connection)
        self.os = OSRepository(self.connection)
        self.sys_unit = SysUnitRepository(self.connection)
        self.tech_devices = TechDevicesRepository(self.connection)