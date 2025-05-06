import sqlite3

class DataBase:
	def __init__(self, db_name='bar.db'):
		self.con = sqlite3.connect(db_name)
		self.load_tables()

	def load_tables(self):
		cur = self.con.cursor()
		cur.executescript("""
			CREATE TABLE IF NOT EXISTS drinks(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				amount INTEGER NOT NULL,
				fortress INTEGER NOT NULL);
			CREATE TABLE IF NOT EXISTS cocktails(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				fortress INTEGER NOT NULL,
				composition TEXT NOT NULL,
				amount INTEGER NOT NULL,
				price INTEGER NOT NULL);
			CREATE TABLE IF NOT EXISTS operations_drinks(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_drinks INTEGER NOT NULL,
				sale INTEGER,
				Replenishment_stocks INTEGER,
				FOREIGN KEY (id_drinks) REFERENCES drinks (id));
			CREATE TABLE IF NOT EXISTS operations_cocktails(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_cocktails INTEGER NOT NULL,
				sale INTEGER,
				Replenishment_stocks INTEGER,
				FOREIGN KEY (id_cocktails) REFERENCES cocktails (id))
			""")

	def add_drinks(self, data: tuple):
		cur = self.con.cursor()
		id_drink = cur.execute(f"SELECT id FROM drinks WHERE name='{data[0]}' AND fortress={data[2]}").fetchone()
		if id_drink is None:
			cur.execute("INSERT INTO drinks VALUES(NULL, ?, ?, ?)", data)
			id_drink = cur.execute(f"SELECT id FROM drinks WHERE name='{data[0]}' AND fortress={data[2]}").fetchone()
		else:
			cur.execute(f"""UPDATE drinks SET
				amount={data[1]}+(SELECT amount FROM drinks WHERE id={id_drink[0]})
				WHERE id={id_drink[0]}""")
		cur.execute(f"INSERT INTO operations_drinks VALUES(NULL, {id_drink[0]}, NULL, {data[1]})")
		self.con.commit()

	def add_cocktails(self, data: tuple):
		cur = self.con.cursor()
		id_cocktail = cur.execute(f"SELECT id FROM cocktails WHERE name='{data[0]}'").fetchone()
		if id_cocktail is None:
			cur.execute("INSERT INTO cocktails VALUES(NULL, ?, ?, ?, ?, ?)", data)
		else:
			cur.execute(f"""UPDATE drinks SET
				amount={data[3]}+(SELECT amount FROM cocktails WHERE id={id_cocktail[0]})
				WHERE id={id_cocktail[0]}""")
		cur.execute(f"""INSERT INTO operations_cocktails VALUES(NULL,
			(SELECT id FROM cocktails WHERE name='{data[0]}'), NULL, {data[3]})""")
		self.con.commit()

	def selling_drinks(self, data: tuple):
		cur = self.con.cursor()
		try:
			out = cur.execute("SELECT id, amount FROM drinks WHERE id=?", (data[0],)).fetchone()
			if out[1] - data[1] < 0:
				print("Такого количество нет на складе")
			else:
				cur.execute("INSERT INTO operations_drinks VALUES(NULL, ?, ?, NULL)", (out[0], data[1]))
				cur.execute("UPDATE drinks SET amount=?-? WHERE id=?", (out[1], data[1], out[0]))
				self.con.commit()
		except:
			print("Напиток не найден!")

	def selling_cocktails(self, data: tuple):
		cur = self.con.cursor()
		try:
			out = cur.execute("SELECT id, amount FROM cocktails WHERE id=?", (data[0],)).fetchone()
			if out[1] - data[1] < 0:
				print("Такого количество нет на складе")
			else:
				cur.execute("INSERT INTO operations_cocktails VALUES(NULL, ?, ?, NULL)", (out[0], data[1]))
				cur.execute("UPDATE cocktails SET amount=?-? WHERE id=?", (out[1], data[1], out[0]))
				self.con.commit()
		except:
			print("Коктель не найден!")

	def view_drinks(self):
		cur = self.con.cursor()
		try:
			cur.execute("SELECT * FROM drinks")
			print("id Имя Количество Крепкость")
			for drink in cur:
				print(drink[0], drink[1], drink[2], drink[3])
		except:
			print("Напитоков нету")

	def view_cocktails(self):
		cur = self.con.cursor()
		try:
			cur.execute("SELECT * FROM cocktails")
			print("id Имя Крепкость Состав Количество Цена")
			for drink in cur:
				print(drink[0], drink[1], drink[2], drink[3], drink[4], drink[5])
		except:
			print("Коктелий нету")

	def __del__(self):
		self.con.close()


def print_action():
	print("1. Добавить напиток")
	print("2. Добавить коктель")
	print("3. Продажа напитка")
	print("4. Продажа коктеля")
	print("5. Показать напитки")
	print("6. Показать коктели")
	print("7. Показать этот список")
	print("8. Закрыть программу")

def main():
	db = DataBase()
	print_action()
	while True:
		try:
			action = int(input("\nВыберете действие: "))
		except ValueError:
			print("\033[31mОшибка ввода!\033[0m")
			return None
		match action:
			case 1:
				name = input("Название напитка: ").lower()
				amount = int(input("Количество напитка: "))
				fortress = int(input("Крепкость напитка: "))
				data = (name, amount, fortress)
				db.add_drinks(data)
			case 2:
				name = input("Название коктеля: ").lower()
				db.view_drinks()
				composition = input("Состав (id_напитка,ингридиент,...): ").split(",")
				with sqlite3.connect("bar.db") as con:
					cur = con.cursor()
					try:
						fortress = cur.execute(f"SELECT fortress FROM drinks WHERE id={composition[0]}").fetchone()
						if fortress is None:
							print("Нет такого напитка")
							composition.pop(0)
							fortress = 0
						else:
							fortress = fortress[0]
					except:
						fortress = 0
				amount = int(input("Количество: "))
				price = int(input("Цена: "))
				composition = ",".join(composition)
				db.add_cocktails((name, fortress, composition, amount, price))
			case 3:
				db.view_drinks()
				id_drink = int(input("\nВведите id напитка: "))
				sell_amount = int(input("Сколько продали напитка: "))
				db.selling_drinks((id_drink, sell_amount))
			case 4:
				db.view_cocktails()
				id_cocktail = int(input("\nВведите id коктеля: "))
				sell_amount = int(input("Сколько продали коктеля: "))
				db.selling_cocktails((id_cocktail, sell_amount))
			case 5:
				db.view_drinks()
			case 6:
				db.view_cocktails()
			case 7:
				print_action()
			case _:
				break

if __name__ == "__main__":
    main()