
def sum_parametrs(list_objects):
    '''Считает сумму зарплаты списка нарядов '''
    lst = []
    for obj in list_objects:
        salary = float(obj.price) * int(obj.quantity) * 1.4
        lst.append(salary)
    return sum(lst)
