
class FlatIterator:

    def __init__(self, list_of_list):
        self.data = list_of_list


    def __iter__(self):
        self.s = [self.data] # храним путь к текущему элементу
        self.idx = [-1] # храним индексы вхождений в подсписки и индекс текущего элемента
        return self


    def __next__(self):
        while(True): # входим в подсписки, пока не найдем простой элемент
            self.idx[-1] += 1

            while self.idx[-1] >= len(self.s[-1]): # список на этом уровне закончился
                del self.idx[-1] # поднимаемся на уровень выше
                del self.s[-1]
                if len(self.idx) == 0: # список путей закончился
                    raise StopIteration
                    return
                else:
                    self.idx[-1] += 1

            item = self.s[-1][self.idx[-1]]
            if isinstance(item, list): # нашли списко среди элементов
                self.s.append(item)
                self.idx.append(-1)
            else:
                return item



def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

##    for s in FlatIterator(list_of_lists_2):
##        print(s)


    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()

