import pyodbc

def insert_to_kab(number: int, street: str, home: str):
    try:
        conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
    )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("insert into Кабинеты (Номер, Улица, Дом) values (?, ?, ?)", number , street, home)
        conn.commit()
        cursor.close()
    except:
        print("Error")
    finally:
        conn.close()


def insert_to_sys_unit(model, invent_num, IP, virtual_IP, kab_code, emp_code):
    try:
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(
            "insert into СистемныеБлоки (Модель, ИнвентарныйНомер, IP, ВиртуальныйIP, Кодкабинета, Кодсотрудника) values (?, ?, ?, ?, ?, ?)",
            model, invent_num, IP, virtual_IP, kab_code, emp_code)
        conn.commit()
        cursor.close()
    except:
        print("Error")
    finally:
        conn.close()

def insert_to_employee(surname, name, patronymic, birthday, gender, post, rank, division, region, phone_number, SNILS):
    try:
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(
            "insert into Сотрудники (Фамилия, Имя, Отчество, ДатаРождения, Пол, Должность, Звание, Подразделение, Регион, Телефон, СНИЛС) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            surname, name, patronymic, birthday, gender, post, rank, division, region, phone_number, SNILS)
        conn.commit()
        cursor.close()
    except:
        print("Error")
    finally:
        conn.close()

def get_id_kab():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT Max(Кодкабинета) FROM Кабинеты')
    last_id = cursor.fetchone()[0]
    print('Последний вставленный идентификатор:', last_id)
    return last_id

def get_id_emp():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT Max(Кодсотрудника) FROM Сотрудники')
    last_id = cursor.fetchone()[0]
    print('Последний вставленный идентификатор:', last_id)
    return last_id

def get_id_sysb():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT Max(КодСистемногоБлока) FROM СистемныеБлоки')
    last_id = cursor.fetchone()[0]
    print('Последний вставленный идентификатор:', last_id)
    return last_id


def insert_to_os(os):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sysb_id = get_id_sysb()
    cursor.execute("insert into ОперационныеСистемы (Наименование, КодСистемногоБлока) values (?, ?)", os, sysb_id)
    conn.commit()
    cursor.close()
    conn.close()


def inset_to_tech(container: tuple):
    #сделать проверку на пустоту контейнера
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\lenovo\PycharmProjects\MVDFinal\MVD.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sysb_id = get_id_sysb()
    for name, mark, sys_num in container:
        cursor.execute("insert into ТехническиеСредства (Наименование, Марка, СерийныйНомер, КодСистемногоБлока) values (?, ?, ?, ?)",
                        name, mark, sys_num, sysb_id)
    conn.commit()
    cursor.close()
    conn.close()






