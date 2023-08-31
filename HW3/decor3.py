import types
import os
from decor2 import logger

log_name = 'gen.log'


@logger(log_name)
def flat_generator(list_of_lists):
    x = 0
    y = 0
    while(x < len(list_of_lists)):
        yield list_of_lists[x][y]
        y += 1
        if y >= len(list_of_lists[x]):
            x += 1
            y = 0



def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    print(list(flat_generator(list_of_lists_1)))
    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    if os.path.exists(log_name):
        os.remove(log_name)

    test_2()
