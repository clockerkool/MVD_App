import os

import pyodbc


def get_db_path():
    # Получаем путь к папке проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    # Строим относительный путь к базе данных
    db_path = os.path.join(project_dir, "MVD.accdb")
    return db_path

def get_id_kab():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT Max(Кодкабинета) FROM Кабинеты')
    last_id = cursor.fetchone()[0]
    print('Последний вставленный идентификатор:', last_id)
    return last_id + 1


def get_id_emp():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT Max(Кодсотрудника) FROM Сотрудники')
    last_id = cursor.fetchone()[0]
    print('Последний вставленный идентификатор:', last_id)
    return last_id

def get_id_sysb():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT Max(КодСистемногоБлока) FROM СистемныеБлоки')
    last_id = cursor.fetchone()[0]
    print('Последний вставленный идентификатор:', last_id)
    return last_id


def update_emp(id, surname, name, patronymic, birthday, gender, post, rank, division, region, phone_number, SNILS):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sql = """
    UPDATE Сотрудники
    SET 
        Фамилия = ?,
        Имя = ?,
        Отчество = ?,
        ДатаРождения = ?,
        Пол = ?,
        Должность = ?,
        Звание = ?,
        Подразделение = ?,
        Регион = ?,
        Телефон = ?,
        СНИЛС = ?
    WHERE
        Кодсотрудника = ?
    """

    # Выполнение оператора UPDATE
    cursor.execute(sql, (surname,
        name,
        patronymic,
        birthday,
        gender,
        post,
        rank,
        division,
        region,
        phone_number,
        SNILS,
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()

def update_sys_unit(model, invent_num, IP, virtual_IP,  emp_code):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()


    sql_update = """
    UPDATE СистемныеБлоки
    SET 
        Модель = ?,
        ИнвентарныйНомер = ?,
        IP = ?,
        ВиртуальныйIP = ?
    WHERE
        Кодсотрудника = ?
    """
    cursor.execute(sql_update, (
        model, invent_num, IP, virtual_IP, emp_code
    ))

    conn.commit()
    cursor.close()
    conn.close()

def update_kab(id_emp, number, street, home):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sql_select = """
    SELECT Кабинеты.Кодкабинета
    FROM Сотрудники
    INNER JOIN (Кабинеты INNER JOIN СистемныеБлоки ON Кабинеты.Кодкабинета = СистемныеБлоки.Кодкабинета) ON Сотрудники.Кодсотрудника = СистемныеБлоки.Кодсотрудника
    WHERE Сотрудники.Кодсотрудника = ?
    """
    cursor.execute(sql_select, (id_emp))
    cabinet = cursor.fetchone()
    print(cabinet)
    if cabinet:
        sql_update = """
        UPDATE Кабинеты
        SET 
            Номер = ?,
            Улица = ?,
            Дом = ?
        WHERE
            Кодкабинета = ?
        """
        cursor.execute(sql_update, (number, street, home, cabinet.Кодкабинета))
        conn.commit()
    else:
        print("Для указанного сотрудника не найдена информация о кабинете")

    cursor.close()
    conn.close()


def update_os(id_emp, os):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sql_select = """
        SELECT ОперационныеСистемы.КодОперационнойСистемы
        FROM Сотрудники INNER JOIN (СистемныеБлоки INNER JOIN ОперационныеСистемы ON СистемныеБлоки.КодСистемногоБлока = ОперационныеСистемы.КодСистемногоБлока) ON Сотрудники.Кодсотрудника = СистемныеБлоки.Кодсотрудника
        WHERE Сотрудники.Кодсотрудника = ?;
        """
    cursor.execute(sql_select, (id_emp))
    o_sys = cursor.fetchone()
    print(o_sys)
    if o_sys:
        sql_update = """
            UPDATE ОперационныеСистемы
            SET 
                Наименование = ?
            WHERE
                КодОперационнойСистемы = ?
            """
        cursor.execute(sql_update, (os , o_sys.КодОперационнойСистемы))
        conn.commit()
    else:
        print("Для указанного сотрудника не найдена информация о кабинете")

    cursor.close()
    conn.close()

def update_tech(id_emp, data):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sql_select = """
        SELECT КодСистемногоБлока
        FROM СистемныеБлоки
        WHERE Кодсотрудника = ?
        """
    cursor.execute(sql_select, (id_emp))
    id_sys_unit = cursor.fetchone()[0]
    print(id_sys_unit)

    sql_select = """
            DELETE FROM ТехническиеСредства
            WHERE КодСистемногоБлока = ?;
            """

    cursor.execute(sql_select, (id_sys_unit))
    conn.commit()
    for name, mark, sys_num in data:
        cursor.execute("insert into ТехническиеСредства (Наименование, Марка, СерийныйНомер, КодСистемногоБлока) values (?, ?, ?, ?)",
                        name, mark, sys_num, id_sys_unit)
    conn.commit()
    cursor.close()
    conn.close()

def delete_emp(id_emp):
    conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    sql_select = """
                DELETE FROM Сотрудники
                WHERE Кодсотрудника = ?;
                """

    cursor.execute(sql_select, (id_emp,))
    conn.commit()
    cursor.close()
    conn.close()




