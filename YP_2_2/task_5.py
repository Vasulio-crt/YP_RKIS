# Создать класс с двумя свойствами. Добавить конструктор с входными
# параметрами. Добавить конструктор, инициализирующий свойства по умолчанию.
# Добавить деструктор, выводящий на экран сообщение об удалении объекта. Написать
# программу, демонстрирующую все возможности класса.
class Human:
	def __init__(self, name="bob", age=20):
		self.name = name
		self.age = age

	def info(self):
		print(f"Имя: {self.name} Возраст: {self.age}")

	def __del__(self):
		print(f"Объект удалён {self.name}")

Tom = Human("tom")
Tom.info()
Eric = Human("Eric", 25)
Eric.info()
Bob = Human()
Bob.info()