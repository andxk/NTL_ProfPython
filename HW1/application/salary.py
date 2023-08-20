# salary

class Salary:

    def __init__(self, base_rate : int):
        self.base_rate = max([base_rate, 15000])

    def calculate_salary(self, post : int):
        if post < 1:
            post = 1
        elif post > 30:
            post = 30

        print(f'Salary = {self.base_rate + post*3000}')
        return


