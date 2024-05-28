from docxtpl import DocxTemplate


def get_tech(name_sys, model_sys, id_sys, address, office_num):
    print(name_sys, model_sys, id_sys, address, office_num)
    doc = DocxTemplate("example_passport.docx")
    context = { 'name_sys' : name_sys, 'model_sys': model_sys, 'id_sys': id_sys,
                'address': address, 'office_num': office_num
                }
    doc.render(context)
    doc.save("tech_passport.docx")

# def example1(name1, name2, name3, name4):
#     doc = DocxTemplate("example_passport.docx")
#     context = {
#                 'name1': name1,
#                 'name2': name2,
#                 'name3': name3,
#                 'name4': name4,
#             }
#     doc.render(context)5
#     doc.save("Заявление.docx")

def get_request(name):
    try:
        doc = DocxTemplate("Письмо.docx")
        context = { 'name' : name}
        doc.render(context)
        print("ALL RIGHT")
        doc.save("Заявление.docx")
        print("Файл успешно сохранен.")
    except Exception as e:
        print("Ошибка при сохранении файла:", e)






