# Создайте класс Calculation, в котором будет одно свойство calculationLine.
# методы: SetCalculationLine который будет который будет изменять значение свойства,
# SetLastSymbolCalculationLine который будет в конец строки прибавлять символ,
# GetCalculationLine который будет выводить значение свойства, GetLastSymbol получение
# последнего символа, DeleteLastSymbol удаление последнего символа из строки
class Calculation:
	def __init__(self, calculationLine: str):
		self.__calculationLine = calculationLine

	def SetCalculationLine(self, newCalculationLine: str):
		self.__calculationLine = newCalculationLine

	def SetLastSymbolCalculationLine(self, lastSymbol):
		self.__calculationLine += str(lastSymbol)[0]

	def GetCalculationLine(self):
		print(self.__calculationLine)

	def GetLastSymbol(self):
		try:
			lastSymbol = self.__calculationLine[-1]
			return lastSymbol
		except IndexError:
			return "\u001b[31mНету символов!\u001b[0m"

	def DeleteLastSymbol(self):
		line = self.__calculationLine
		if len(line) != 0:
			self.__calculationLine = line[:len(line)-1]
		else:
			print("\u001b[31mНету символов!\u001b[0m")

ss = Calculation("12345asd")
ss.DeleteLastSymbol()
ss.SetLastSymbolCalculationLine("99")
ss.GetCalculationLine()
print(ss.GetLastSymbol())
ss.SetCalculationLine("9876")
ss.GetCalculationLine()