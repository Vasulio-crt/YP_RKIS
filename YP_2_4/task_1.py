import sqlite3
import re

class Students:
	def __init__(self, first_name, last_name, patronymic, group, grades):
		self.first_name = first_name
		self.last_name = last_name
		self.patronymic =  None if patronymic == '' else patronymic
		self.group = group
		self.grades = grades


class DataBase:
	def load_table(self):
		with sqlite3.connect("main.db") as con:
			cur = con.cursor()
			cur.execute("""
				CREATE TABLE IF NOT EXISTS students(
					id INTEGER PRIMARY KEY AUTOINCREMENT,
		            first_name TEXT NOT NULL,
		            last_name TEXT NOT NULL,
		            patronymic TEXT NULL,
	                group_st TEXT NOT NULL,
		            grades TEXT NOT NULL)
				""")
	
	def add_student(self, stud):
		with sqlite3.connect("main.db") as con:
			cur = con.cursor()
			data = (stud.first_name, stud.last_name, stud.patronymic, stud.group, stud.grades)
			cur.execute("INSERT INTO students(first_name, last_name, patronymic, group_st, grades) VALUES(?, ?, ?, ?, ?)", data)
			con.commit()

	def view_all_students(self):
		with sqlite3.connect("main.db") as con:
			cur = con.cursor()
			cur.execute("SELECT id, first_name, last_name, patronymic, group_st FROM students")
			print("id\tИмя\tФамилия\tОтчество\tГруппа")
			for student in cur:
				print(f"{student[0]}\t{student[1]}\t{student[2]}\t{"" if student[3] == None else student[3]}\t{student[4]}")

	def view_one_student(self):
		with sqlite3.connect("main.db") as con:
			cur = con.cursor()
			cur.execute("SELECT id, first_name, last_name FROM students")
			print("id\tИмя\tФамилия")
			for student in cur:
				print(f"{student[0]}\t{student[1]}\t{student[2]}")

			id_stud = int(input("Введите id студента: "))
			cur.execute(f"SELECT * FROM students WHERE id={id_stud}")
			cur = cur.fetchone()

			print(f"\nИмя - {cur[1]}\nФамилия - {cur[2]}\nОтчество - {cur[3]}\nГруппа - {cur[4]}")
			ratings = tuple(map(int, cur[5].split(",")))
			print(f"Оценки - {ratings[0],ratings[1],ratings[2],ratings[3]}; средний балл = {sum(ratings)/4}")

	def edit_student(self):
		with sqlite3.connect("main.db") as con:
			cur = con.cursor()
			id_stud = int(input("Введите id студента: "))
			stud = cur.execute(f"SELECT * FROM students WHERE id={id_stud}").fetchone()
			if len(stud) == 0:
				print("Нет такого id")
				return None

			data_edit = []
			for i in range(1, len(stud)-1):
				data = input(f"Прошлые данные {stud[i]}: ")
				if data == "":
					data_edit.append(stud[i])
				else:
					data_edit.append(data)
			data = input(f"Оценки студента ({stud[5]}): ")
			if data != "":
				while not re.match(r"^[2-5],[2-5],[2-5],[2-5]$", data):
					data = input("Оценки студента (4,4,4,4): ")
				data_edit.append(data)
			else:
				data_edit.append(stud[5])
			data_edit.append(id_stud)
			data_edit = tuple(data_edit)

			cur.execute("""UPDATE students SET first_name=?, last_name=?, patronymic=?,
				group_st=?, grades=? WHERE id=?""", data_edit)
			con.commit()

	def delete_student(self):
		with sqlite3.connect("main.db") as con:
			cur = con.cursor()
			self.view_all_students()
			id_stud = int(input("Введите id студента: "))
			cur.execute(f"DELETE FROM students WHERE id={id_stud}")
			con.commit()

	def view_average_score_students(self):
		with sqlite3.connect("main.db") as con:
			cur = con.cursor()
			cur_copy = cur.execute("SELECT DISTINCT group_st FROM students").fetchall()
			for grop in cur_copy:
				print(grop[0], end="  ")
			group = input("\nВведите номер группы: ")
			cur_copy = cur.execute(f"SELECT first_name, last_name, grades FROM students WHERE group_st={group}").fetchall()
			print("Имя\tФамилия\tСр. балл")
			for stud in cur_copy:
				ratings = tuple(map(int, stud[2].split(",")))
				print(f"{stud[0]}\t{stud[1]}\t{sum(ratings)/4}")


# SELECT DISTINCT group_st FROM students

def print_action():
	print("1. Добавление нового студента")
	print("2. Просмотр всех студентов")
	print("3. Просмотр одного студента, включая его средний балл")
	print("4. Редактирование студента")
	print("5. Удаление студента")
	print("6. Просмотр среднего балла студентов у конкретной группы")
	print("7. Показать этот список")
	print("8. Закрыть программу")

def main():
	db = DataBase()
	db.load_table()
	print_action()
	while True:
		try:
			action = int(input("\nВыберете действие: "))
		except ValueError:
			print("\033[31mОШИБКА ВВОДА\033[0m❗")
			return None
		match action:
			case 1:
				first_name = input("Имя студента: ")
				last_name = input("Фамилию студента: ")
				patronymic = input("Отчество студента: ")
				group = input("Группа студента: ")
				grades = input("Оценки студента (5,5,5,5): ")
				while not re.match(r"^[2-5],[2-5],[2-5],[2-5]$", grades):
					grades = input("Оценки студента (4,4,4,4): ")
				student = Students(first_name, last_name, patronymic, group, grades)
				db.add_student(student)
			case 2:
				db.view_all_students()
			case 3:
				db.view_one_student()
			case 4:
				db.edit_student()
			case 5:
				db.delete_student()
			case 6:
				db.view_average_score_students()
			case 7:
				print_action()
			case _:
				break

if __name__ == "__main__":
	main()