# Описать класс, реализующий счетчик, который может увеличивать или
# уменьшать свое значение на единицу. Предусмотреть инициализацию счетчика со
# значением по умолчанию и произвольным значением. Счетчик имеет два метода:
# увеличения и уменьшения, — и свойство, позволяющее получить его текущее состояние.
# Написать программу, демонстрирующую все возможности класса.
class Counter:
	def __init__(self, count=0):
		self.count = count

	def increase(self):
		self.count += 1

	def	decrease(self):
		self.count -= 1

	def info(self):
		print("counter =", self.count)

count = Counter(5)
count.info()
count.increase()
count.increase()
count.info()
count.decrease()
count.info()