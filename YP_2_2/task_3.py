# Создайте класс с двумя свойствами для хранения целых чисел. Добавить
# метод для вывода на экран и метод для изменения этих чисел. Добавить метод, который
# находит сумму значений этих чисел, и метод который находит наибольшее значение из
# этих чисел. Написать программу, демонстрирующую все возможности класса.
class Number:
	def __init__(self, num1, num2):
		self.num1 = num1
		self.num2 = num2

	def print_num(self):
		print(f"number_1: {self.num1}, number_2: {self.num2}")
		print("Есть метод sum_number, для нахождения сумм чисел класса\n")

	def sum_number(self):
		print("Сумма чисел =", self.num1+self.num2)

	def large_number(self):
		if self.num1 > self.num2:
			print(f"number_1 > number_2 ({self.num1} > {self.num2})")
		else:
			print(f"number_2 > number_1 ({self.num2} > {self.num1})")

numbers = Number(56, 100)
numbers.print_num()
numbers.large_number()