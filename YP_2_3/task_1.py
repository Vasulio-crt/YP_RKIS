# Реализуйте класс Worker, который будет иметь следующие свойства: name,
# surname, rate (ставка за день работы), days (количество отработанных дней). Также класс
# должен иметь метод GetSalary(), который будет выводить зарплату работника. Зарплата -
# это произведение ставки rate на количество отработанных дней days
class Worker:
	def __init__(self, name, surname, rate, days):
		self.name = name
		self.surname = surname
		self.rate = rate
		self.days = days

	def GetSalary(self):
		print("Зарплата", self.rate * self.days)

Bob = Worker("Bob", "Ortiz", 500, 25)
Bob.GetSalary()