# Модифицируйте класс Worker из предыдущей задачи, сделайте все его
# свойства приватными, а для их чтения сделайте методы-геттеры;
class Worker:
	def __init__(self, name, surname, rate, days):
		self.__name = name
		self.__surname = surname
		self.__rate = rate
		self.__days = days

	def GetSalary(self):
		print("Зарплата", self.__rate * self.__days)

	def getName(self):
		return self.__name

	def getSurname(self):
		return self.__surname

	def getRate(self):
		return self.__rate

	def getDays(self):
		return self.__days

Bob = Worker("Bob", "Ortiz", 500, 25)
print(f"name: {Bob.getName()}, surname: {Bob.getSurname()}\nrate: {Bob.getRate()}, days: {Bob.getDays()}")
Bob.GetSalary()