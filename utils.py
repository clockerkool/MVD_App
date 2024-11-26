import os
import pyodbc

def get_db_path():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_dir, "MVD.accdb")


# def get_id_sysb():
#     conn_str = (
#         r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + get_db_path() + ';'
#     )
#     conn = pyodbc.connect(conn_str)
#     cursor = conn.cursor()
#     cursor.execute('SELECT Max(КодСистемногоБлока) FROM СистемныеБлоки')
#     last_id = cursor.fetchone()[0]
#     print('Последний вставленный идентификатор:', last_id)
#     return last_id