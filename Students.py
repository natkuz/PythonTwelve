# Создайте класс студента
# Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв
# Названия предметов должны загружаться из файла csv при создании экземпляра
# Другие предметы в экземпляре недопустимы
# Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100)
# Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых

import csv
import json
import os

class NameValidation:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value: str):
        if value.istitle() and value.isalpha():
            setattr(instance, self.name, value)
        else:
            raise ValueError


class Student:

    last_name = NameValidation()
    first_name = NameValidation()
    patronymic = NameValidation

    # __slots__ = ('_first_name', '_last_name', '_patronymic')

    def __init__(self, last_name, first_name, patronymic):
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.student = [self.last_name + ' ' + self.first_name + ' ' + self.patronymic]
        if not os.path.exists('students.json'):
            data_students = []
            with open('students.json', 'w', encoding='UTF-8') as file:
                json.dump(data_students, file, indent=4, ensure_ascii=False)
        if os.path.exists('students.json'):
            ch = int(input(f"Если студенту {self.student[0]} нужно поставить оценку, введите '1',\n"
                           f"если внести результат теста, введите '2',\n"
                           f"если вывести средний балл студента, введите '3',\n"
                           f"если вывести средний балл по тестам по предмету, введите '4'\n"
                           f"если добавить студента в список, введите '5': "))
            match ch:
                case 1:
                    with open('students.json', 'r', encoding='UTF-8') as st_file:
                        data_students = json.load(st_file)
                        if self.student[0] in data_students:
                            self.points(self.student)
                        else:
                            data_students.extend(self.student)
                            self.points(self.student)
                            with open('students.json', 'w', encoding='UTF-8') as file:
                                json.dump(data_students, file, indent=4, ensure_ascii=False)
                case 2:
                    with open('students.json', 'r', encoding='UTF-8') as st_file:
                        data_students = json.load(st_file)
                        if self.student[0] in data_students:
                            self.test_result(self.student)
                        else:
                            data_students.extend(self.student)
                            self.test_result(self.student)
                case 3:
                    self.gpa(self.student)
                case 4:
                    self.gpa_tests_subject(self.student)
                case 5:
                    self.new_student(self.student)
                case _:
                    print('Ошибка ввода')

    # def __enter__(self):
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     file_csv = open('subject.csv', 'r', newline='', encoding='UTF-8')
    #     file_json = open('journal.json', 'w', encoding='UTF-8')
    #     subjects_csv = csv.reader(file_csv)
    #     self.subjects = {}
    #     for line in subjects_csv:
    #         self.subjects[line[0]] = []
    #     json.dump(self.subjects, file_json, indent=4, ensure_ascii=False)
    #     file_json.close()
    #     file_csv.close()

    def new_student(self, st):
        with open('students.json', 'r', encoding='UTF-8') as st_file:
            data_students = json.load(st_file)
            if st[0] in data_students:
                print(f'Студент {st[0]} уже есть в списке')
            else:
                data_students.extend(st)
                print(f'Студент внесен в список')
        with open('students.json', 'w', encoding='UTF-8') as file:
            json.dump(data_students, file, indent=4, ensure_ascii=False)

    def sudject(self):
        subj = []
        with open('subject.csv', 'r', newline='', encoding='UTF-8') as file_csv:
            subjects_csv = csv.reader(file_csv)
            subjects = {}
            for line in subjects_csv:
                subjects[line[0]] = []
        for key in subjects.keys():
            subj.append(key)
        return subj

    def points(self, st):
        MIN_POINT = 2
        MAX_POINT = 5
        while True:
            subject = input(f"Введите предмет, по которому надо поставить оценку студенту {st[0]}: ")
            if not subject in self.sudject():
                print(f'Предмета {subject} нет. Попробуйте еще раз.')
            else:
                break
        while True:
            point = input("Введите оценку от 2 до 5: ")
            if not point.isdigit() or not MIN_POINT <= int(point) <= MAX_POINT:
                print(f'Нельзя поставить оценку {point}. Попробуйте еще раз.')
            else:
                break
        if not os.path.exists('journal.json'):
            with open('subject.csv', 'r', newline='', encoding='UTF-8') as file_csv:
                subjects_csv = csv.reader(file_csv)
                subjects = {}
                for line in subjects_csv:
                    subjects[line[0]] = []
            with open('journal.json', 'w', encoding='UTF-8') as file:
                json.dump(subjects, file, indent=4, ensure_ascii=False)
        if os.path.exists('journal.json'):
            with open('journal.json', 'r', encoding='UTF-8') as jl:
                journal = json.load(jl)
                for key, item in journal.items():
                    if key == subject:
                        if not item:
                            journal[key] = [[*st, point]]
                        else:
                            journal[key].append([*st, point])
                print(journal)
            with open('journal.json', 'w', encoding='UTF-8') as new_point:
                json.dump(journal, new_point, indent=4, ensure_ascii=False)

    def test_result(self, st):
        MIN_RESULT = 0
        MAX_RESULT = 100
        while True:
            subject = input(f"Введите предмет, по которому надо внести результат теста студента {st[0]}: ")
            if not subject in self.sudject():
                print(f'Предмета {subject} нет. Попробуйте еще раз.')
            else:
                break
        while True:
            test_res = input(f"Введите результат теста от {MIN_RESULT} до {MAX_RESULT}: ")
            if not test_res.isdigit() or not MIN_RESULT <= int(test_res) <= MAX_RESULT:
                print(f'Нельзя поставить оценку {test_res}. Попробуйте еще раз.')
            else:
                break
        if not os.path.exists('test_result.json'):
            with open('subject.csv', 'r', newline='', encoding='UTF-8') as file_csv:
                subjects_csv = csv.reader(file_csv)
                subjects = {}
                for line in subjects_csv:
                    subjects[line[0]] = []
            with open('test_result.json', 'w', encoding='UTF-8') as file:
                json.dump(subjects, file, indent=4, ensure_ascii=False)
        if os.path.exists('test_result.json'):
            with open('test_result.json', 'r', encoding='UTF-8') as tr:
                test_result = json.load(tr)
                for key, item in test_result.items():
                    if key == subject:
                        if not item:
                            test_result[key] = [[*st, test_res]]
                        else:
                            test_result[key].append([*st, test_res])
                print(test_result)
            with open('test_result.json', 'w', encoding='UTF-8') as new_res:
                json.dump(test_result, new_res, indent=4, ensure_ascii=False)

    def gpa(self, st):
        if not os.path.exists('journal.json'):
            raise FileNotFoundError('Еще нет ни одной оценки')
        else:
            with open('journal.json', 'r', encoding='UTF-8') as jl:
                journal = json.load(jl)
                student_points = 0
                count = 0
                for key, items in journal.items():
                    for item in items:
                        if item[0] == st[0]:
                            student_points += int((item[1]))
                            count += 1
                if count == 0:
                    print(f'У студента {st[0]} нет оценок')
                else:
                    print(f'Средний балл студента {st[0]} = {student_points / count}')

    def gpa_tests_subject(self, st):
        if not os.path.exists('test_result.json'):
            raise FileNotFoundError('Еще нет ни одного результата теста')
        else:
            with open('test_result.json', 'r', encoding='UTF-8') as tr:
                test_res = json.load(tr)
                while True:
                    subject = input(f"Введите предмет, по которому надо вывести средний балл тестов студента {st[0]}: ")
                    if not subject in self.sudject():
                        print(f'Предмета {subject} нет. Попробуйте еще раз.')
                    else:
                        break
                student_res_tests = 0
                count = 0
                for key, items in test_res.items():
                    if key == subject:
                        for item in items:
                            if item[0] == st[0]:
                                student_res_tests += int((item[1]))
                                count += 1
                if count == 0:
                    print(f'У студента {st[0]} нет результатов теста по предмету {subject}')
                else:
                    print(f'Средний балл тестов по предмету {subject} студента {st[0]} = {student_res_tests / count}')

    def __repr__(self):
        """Вывод инфо на печать для программиста"""
        return f'Student({self.first_name}, {self.last_name}, {self.patronymic})'

    def __str__(self):
        """Вывод инфо для пользователя"""
        return f'Student: {self.student})'


st1 = Student('Васильева', 'Татьяна', 'Павловна')