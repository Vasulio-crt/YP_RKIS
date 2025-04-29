# Создайте класс с именем Student, содержащий свойства: фамилия, дата
# рождения, номер группы, успеваемость (массив из пяти элементов). Добавить возможность
# изменения фамилии, даты рождения и номера группы. Добавить возможность вывода
# информации о студенте, фамилия и дата рождения которого введены пользователем.
# Написать программу, демонстрирующую все возможности класса.
class Student:
    def __init__(self, lastName, date, groupNumber, progress: list):
        self.lastName = lastName
        self.date = date
        self.groupNumber = groupNumber
        if len(progress) != 5:
            for _ in range(5-len(progress)):
                progress.append(0)
            self.progress = progress
        else:
            self.progress = progress

    def edit_last_name(self, newLastName):
        self.lastName = newLastName

    def edit_date(self, newDate):
        self.date = newDate

    def edit_groupNumber(self, newGroupNumber):
        self.groupNumber = newGroupNumber

    def print_info(self):
        print("\nФамилия:", self.lastName)
        print("Дата рождения:", self.date)
        print("Группа:", self.groupNumber)
        print("Оценки:", self.progress)

last_name = input("Введите фамилию: ")
date = input("Введите дату(DD.MM.YYYY): ")
group_number = int(input("Введите номер группы: "))

Carol = Student(last_name, date, group_number, [4, 5, 5, 4, 4])
Carol.print_info()
Carol.edit_date("20.06.2010")
Carol.edit_last_name("Mason")
Carol.edit_groupNumber(632)
Carol.print_info()