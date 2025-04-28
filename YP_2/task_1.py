J = input("Введите строку J: ")
S = input("Введите строку S: ")
count = 0
for j in J:
	for s in S:
		if j == s:
			count += 1

print(count)