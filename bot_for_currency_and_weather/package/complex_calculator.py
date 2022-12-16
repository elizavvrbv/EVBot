def calculation(firstnum, operation, secondnum):
    if operation == '+':
        res = firstnum + secondnum
        return res
    elif operation == '-':
        res = firstnum - secondnum
        return res
    elif operation == '*':
        res = firstnum * secondnum
        return res
    elif operation == '/':
        if secondnum == 0:
            return "Ошибка! Деление на ноль"
        else:
            res = firstnum / secondnum
            result = round(res, 3)
            return result
    else:
        return "Не удалось распознать операцию"
