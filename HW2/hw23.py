

class FlatIterator:

    def __init__(self, list_of_list):
        self.data = list_of_list


    def __iter__(self):
        self.idx = 0    # текущий индекс элемента
        self.cnt = -1   # счетчик для поиска
        return self


    def get_elem(self, s):
        # Перебираем списки пока не насчитаем нужный порядковый номер элемента
        for e in s:
            if isinstance(e, list):
                x = self.get_elem(e)
                if x != e:      # элемент найден
                    return x
                else:           # локальный список закончился
                    continue
            else:
                self.cnt += 1
                if self.cnt >= self.idx:
                    self.idx += 1
                    self.cnt = -1
                    return e    # найденный элемент всегда выходит из этого места
                else:
                    continue

        if s == self.data:
            raise StopIteration
        else:
            return s # индикатор конца локального списка


    def __next__(self):
        item = self.get_elem(self.data)

        return item




def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]


##    for s in FlatIterator(list_of_lists_2): print(s)


    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()

