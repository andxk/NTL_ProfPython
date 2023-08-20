import numpy as np
from datetime import datetime
from application.db.people import get_employees
from application.salary import Salary


if __name__ == '__main__':

    print(datetime.date(datetime.now()))

    get_employees(1)

    sal = Salary(30000)
    sal.calculate_salary(15)

    print()


    # Пример использования пакета 'numpy'
    x = np.arange(15).reshape(3, 5)
    print(x)


