def combination_sum(candidates, target):
    candidates.sort()
    result = []
    
    def backtrack(start, mas, target):
        if target == 0:
            result.append(mas)
            return
        if target < 0:
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            backtrack(i + 1, mas + [candidates[i]], target - candidates[i])
    
    backtrack(0, [], target)
    return result

candidates = list(map(int, input("Введите массив:\n").split()))
target = int(input("Введите target: "))
print(combination_sum(candidates, target))

#10 1 2 7 6 1 5  8