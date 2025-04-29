candidates = list(map(int, input("Введите массив:\n").split()))
target = int(input("Введите target: "))
candidates.sort()
result = []

def candidates_sum(start, mas, target):
    if target == 0:
        result.append(mas)
        return
    if target < 0:
        return
    for i in range(start, len(candidates)):
        if i > start and candidates[i] == candidates[i - 1]:
            continue
        candidates_sum(i + 1, mas + [candidates[i]], target - candidates[i])

candidates_sum(0, [], target)
print(result)
#10 1 2 7 6 1 5  8