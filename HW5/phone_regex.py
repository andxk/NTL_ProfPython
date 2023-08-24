import re
from pprint import pprint
import csv



def read_csv(file_name):
    ''' Читаем адресную книгу в формате CSV в список contacts_list'''
    with open(file_name, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
##    pprint(contacts_list)
    return contacts_list



def write_csv(file_name, contacts_list):
    ## Код для записи файла в формате CSV:
    with open(file_name, "w", newline="") as f:
    ##with open("phonebook2.csv", "w", newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)



def phone_fix(contacts_list, col:int):
    ''' Исправление телефонов в столбце "col" '''
    #функция изменяет переданный ей список
    pattern = r"(\+7|8)\s?(\((\d+)\)|(\d{3}))\W?(\d+)\W*(\d{2})\W*(\d{2})(\W*(доб\.)\W*(\d{4})\W*)?"
    replace = r"+7(\3\4)\5\6\7 \9\10"
    ##replace = r"+7(\3\4)\5\6\7 доб.\10"
    pattern = re.compile(pattern)

    for idx, row in enumerate(contacts_list):
        contacts_list[idx][col] = pattern.sub(replace, row[col]).strip()



def names_fix(contacts_list):
    ''' Заполняем ФИО первые три столбца '''
    #функция изменяет переданный ей список
    for idx, row in enumerate(contacts_list):
        fio = ' '.join(row[:3])
        fio = fio.strip().split(' ')
        contacts_list[idx][:len(fio)] = fio



def merge_row (row1, row2, mstart=0) -> list:
    '''
        Слияние подстрок в списках row1, row2
        mstart - индекс первой обрабатываемой подстроки в списке
    '''
    res = row1
    for i, (a ,b) in enumerate (zip(row1[mstart:], row2[mstart:])):
        i += mstart
        if a == b:
            continue
        elif a in b:
            res[i] = b
        elif b in a:
            res[i] = a
        else:
            res[i] = a + ' ' + b
    return res



def doubles_fix (contacts_list, comp_col1=0, comp_col2=1, merge_start_col=2):
    '''
    Слияние и удаление строк с дублирующимися именами
    comp_col1, comp_col2 - столбцы Имя и Фамилия, где должны совпасть данные в разных строках
    merge_start_col - с какого столбца начинать слияние
    '''
    idx = 0
    while idx < len(contacts_list):
        r1 = contacts_list[idx]
        idy = idx+1
        while idy < len(contacts_list):
            r2 = contacts_list[idy]
##            if r1[id_ln] == r2[id_ln] and r1[id_fn] == r2[id_fn]:
            if r1[comp_col1] == r2[comp_col1] \
            and r1[comp_col2] == r2[comp_col2]:
##                contacts_list[idx] = merge_row(r1, r2, id_sn)
                contacts_list[idx] = merge_row(r1, r2, merge_start_col)
                del contacts_list[idy]
                continue
            idy += 1
        idx += 1




if __name__ == '__main__':

    # Номера столбцов
    id_ln = 0
    id_fn = 1
    id_sn = 2
    id_ph = 5

    contacts_list = read_csv("phonebook_raw.csv")

    phone_fix(contacts_list, id_ph)

    names_fix(contacts_list)

    doubles_fix(contacts_list, id_fn, id_ln, id_sn)

    write_csv("phonebook.csv", contacts_list)

##    print('**********************************')
    pprint(contacts_list)








