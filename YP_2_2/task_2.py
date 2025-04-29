# Создайте класс с именем Train, содержащий свойства: название пункта
# назначения, номер поезда, время отправления. Добавить возможность вывода
# информации о поезде, номер которого введен пользователем. Написать программу,
# демонстрирующую все возможности класса.
class Train:
	def __init__(self, destination, trainNumber, departure):
		self.destination = destination
		self.trainNumber = trainNumber
		self.departure = departure

	def train_info(self):
		print("Пункт назначения:", self.destination)
		print("номер поезда:", self.trainNumber)
		print("Время отправления:", self.departure, "\n")

def find_train(number, trains):
	for train in trains:
		if train.trainNumber == num_train:
			train.train_info()
			return True
	return False


trains = [Train("Москва", 315, "08:45"),
        Train("Томск", 86, "12:30"),
        Train("Казань", 17, "15:15"),
        Train("Новосибирск", 54, "20:00")]

for train in trains:
	train.train_info()

num_train = int(input("Введите номер поезда: "))
find = find_train(num_train, trains)
if not find:
	print("Номер поезда не найден") 
	