def meeting(mas):
	for i in range(len(mas)):
		for j in range(i+1, len(mas)):
			if mas[i] == mas[j]:
				return True
	return False

nums = list(map(int, input("Введите массив:\n").split()))
print(meeting(nums))