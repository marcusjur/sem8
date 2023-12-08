"""
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
"""

from os.path import exists
from csv import DictReader, DictWriter
import re


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class InfoNameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise InfoNameError("Не валидное имя")
            else:
                is_valid_first_name = True
        except InfoNameError as err:
            print(err)
            continue

    last_name = "Иванов"

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


def create_file(file_name):
    # with - Менеджер контекста
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def replace_lines(source_filename: str, destination_filename: str, line_number: int = 0):
    """

    :param source_filename:
    :param destination_filename:
    :param line_number:
    :return:
    """

    try:
        with open(source_filename, 'r', encoding='utf-8') as source_data:
            source_lines = source_data.readlines()
            source_line = source_lines[line_number]
            source_data.close()

        with open(destination_filename, 'w', encoding='utf-8') as destination_data:
            destination_lines = destination_data.readlines()
            destination_lines.append(source_line)
            destination_data.writelines(destination_lines)
            destination_data.close()
    except FileNotFoundError:
        raise FileNotFoundError('Invalid file name')
    except UnicodeDecodeError:
        raise ValueError('Selected file is not UTF-8 formatted')


def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


file_name = 'phone.csv'


def main():
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*read_file(file_name))
        elif bool(re.compile("replace", re.IGNORECASE).match(command)):
            destination_file = input('Enter destination filename')
            source_file = input('Enter source filename')
            line_num = int(input('Enter line number'))

            replace_lines(destination_file, source_file, line_num)


if __name__ == "__main__":
    main()
