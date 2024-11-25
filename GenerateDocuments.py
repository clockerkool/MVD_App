from abc import ABC, abstractmethod
from docxtpl import DocxTemplate
from docx import Document
from Constants.FileNames import FileNames

class IGenerateFile(ABC):
    @abstractmethod
    def generate_file(self, data: list | str) -> None:
        pass
    
class ICreator:
    @abstractmethod
    def create(self) -> IGenerateFile:
        pass


class GenerateRequestDocx(IGenerateFile):
    def generate_file(self, data: list | str) -> None:
        try:
            doc = DocxTemplate("Письмо.docx")
            context = {'name': data}
            doc.render(context)
            doc.save(FileNames.RequestFileName)
            print("Файл успешно сохранен.")
        except Exception as e:
            print("Ошибка при сохранении файла:", e)

class GenerateTechDevicesDocx(IGenerateFile):
    def generate_file(self, data: list | str) -> None:
        """Функция для заполнения технических средств с учётом количества"""
        doc = Document('example_passport.docx')

        # Доступ к таблице
        table = doc.tables[0]
        for i, item in enumerate(data):
            # Добавьте новую строку в таблицу
            row = table.add_row()

            row.cells[0].text = str(i + 1)  # Номер строки
            row.cells[1].text = item['name_sys']
            row.cells[2].text = item['model_sys']
            row.cells[3].text = item['id_sys']
            row.cells[4].text = f"{item['address']}, кб. № {item['office_num']}"

            # Добавить новую строку в конец таблицы
            last_row = table.add_row()
            # Объединить все ячейки в новой строке
            table.cell(last_row._index, 0).merge(table.cell(last_row._index, table._column_count - 1))
            # Добавить текст в объединенную ячейку
            last_row.cells[0].add_paragraph("Периферийное оборудование: клавиатура, \
                                            манипулятор <мышь>, монитор, принтер, WEB-камера, колонки.")

        doc.save(FileNames.TechPassportFileName)


class RequestFileCreator(ICreator):
    def create(self) -> IGenerateFile:
        return GenerateRequestDocx()

class TechDevicesFileCreator(ICreator):
    def create(self) -> IGenerateFile:
        return GenerateTechDevicesDocx()


