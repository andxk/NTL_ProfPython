class FlatIterator:

    def __init__(self, list_of_list):
        self.inlist = list_of_list

    def __iter__(self):
        self.x = 0
        self.y = -1
        return self

    def __next__(self):
        self.y += 1
        if self.y >= len(self.inlist[self.x]):
            self.x += 1
            self.y = 0
            if self.x >= len(self.inlist):
                raise StopIteration
        item = self.inlist[self.x][self.y]
        return item



def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]



if __name__ == '__main__':
    test_1()

