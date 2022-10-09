lst1 = [1, 2, 3, 4]
lst2 = ['a', 'b', 'c', 'd']


def make_dict(lst_key, lst_value):
    dct = {}
    if len(lst_key) >= len(lst_value):
        for i in range(len(lst_value)):
            dct[lst_key[i]] = lst_value[i]
        for i in range(len(lst_value), len(lst_key)):
            dct[lst_key[i]] = None
    else:
        for i in range(len(lst_key)):
            dct[lst_key[i]] = lst_value[i]
    return dct

print(make_dict(lst1, lst2))

# def calculate(number1, number2, operation):
#     if operation == '+':
#         return number1 + number2
#     elif operation == '-':
#         return number1 - number2
#     elif operation == '*':
#         return number1 * number2
#     elif operation == '/':
#         return number1 / number2
#     else:
#         return 'Неизвестная операция'

