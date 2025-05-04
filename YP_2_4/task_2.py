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
			cur.execute("UPDATE drinks SET amount={data[1]} WHERE id={id_drink}")
		cur.execute(f"INSERT INTO operations_drinks VALUES(NULL, {id_drink[0]}, NULL, {data[1]})")
		self.con.commit()

	def view_drinks(self):
		cur = self.con.cursor()
		cur.execute("SELECT * FROM drinks")
		for drink in cur:
			print(drink[0], drink[1], drink[2], drink[3])

	def view_cocktails(self):
		cur = self.con.cursor()
		cur.execute("SELECT * FROM drinks")
		for drink in cur:
			print(drink[0], drink[1], drink[2], drink[3], drink[4])

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