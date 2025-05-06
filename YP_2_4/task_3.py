from datetime import datetime
import sqlite3
import psutil
from psutil._common import bytes2human

class DataBase:
	def __init__(self, db_name="system.db"):
		self.con = sqlite3.connect(db_name)
		self.load_tables()

	def load_tables(self):
		cur = self.con.cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS monitor(
				id INTEGER PRIMARY KEY,
				cpu TEXT NOT NULL,
				ram TEXT NOT NULL,
				dick TEXT NOT NULL)
			""")

	def add_monitor(self, data: tuple):
		cur = self.con.cursor()
		data = (int(data[0]), str(data[1]), str(data[2]), str(data[3]))
		cur.execute("INSERT INTO monitor VALUES(?, ?, ?, ?)", data)
		self.con.commit()

	def view_monitor(self):
		cur = self.con.cursor()
		cur.execute("SELECT * FROM monitor")
		print("CPU\tRAM\tDICK\ttime")
		for data in cur:
			print(f"{data[1]}%\t{data[2]}\t{data[3]}%\t{datetime.fromtimestamp(data[0])}")

	def __del__(self):
		self.con.close()

def print_action():
	print("1. Мониторинг системы")
	print("2. Посметреть все данные о мониторинге системы")
	print("3. Закрыть программу")

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
				data = (datetime.now().timestamp(),
					psutil.cpu_percent(interval=0.5),
					bytes2human(psutil.virtual_memory().active),
					psutil.disk_usage('/').percent)
				print(f"\nCPU: {data[1]}%")
				print(f"RAM: {psutil.virtual_memory().percent}% {data[2]}")
				print(f"DISK: {data[3]}%")
				db.add_monitor(data)
			case 2:
				db.view_monitor()
			case _:
				break

if __name__ == "__main__":
    main()