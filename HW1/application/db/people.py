# people

def get_employees(id : int):
    ''' id = 1..3 '''
    emps = ['Иванов', 'Петров', 'Сидоров']
    if id < 1:
        print('Нет такого работника')
        return

    if (id > len(emps)):
        id = id % len(emps)

    print (emps[id-1])


