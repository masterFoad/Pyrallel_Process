import unittest

from tfrq import tfrq, tfrq_generator


def greet(name="", greeting="Hello"):
    return f"{greeting}, {name}!"


def multiply(*args):
    result = 1
    for number in args:
        result *= number
    return result


def square(n):
    return n * n


def calculate_sum_of_pairs(list_of_pairs):
    results = []
    for pair in list_of_pairs:
        results.append(sum(pair))

    return results


def huge_list_of_data_to_process(data_list):
    params = []

    for data_row in data_list:
        params.append((data_row[0], data_row[1]))

    list_of_results_for_all_pairs = tfrq(calculate_sum_of_pairs, params)

    list_of_results_for_all_pairs = sum(list_of_results_for_all_pairs, [])
    return list_of_results_for_all_pairs


def huge_list_of_data_to_process_custom_executor(data_list):
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=2) as c_executor:
        params = []

        for data_row in data_list:
            params.append((data_row[0], data_row[1]))

        list_of_results_for_all_pairs = tfrq(calculate_sum_of_pairs, params, custom_executor=c_executor)

        list_of_results_for_all_pairs = sum(list_of_results_for_all_pairs, [])
        return list_of_results_for_all_pairs


class MyTestCase(unittest.TestCase):
    def test_parallel_print(self):
        params = ["Hello", "World", "!"]
        func = print
        tfrq(func=func, params=params, num_cores=3, operator="*")
        # H e l l o
        # !
        # W o r l d ---- notice now it is func(*args) - that is causing the spaces.

        params = ["Hello", "World", "!"]
        func = print
        tfrq(func=func, params=params, num_cores=3)
        # Hello
        # World
        # !

    def test_parallel_huge_data(self):
        input_list = [[1, 2], [3, 4], [5, 5], [6, 7]]
        list_of_results_for_all_pairs = tfrq(sum, input_list, num_cores=1)
        print(list_of_results_for_all_pairs)  # [[3], [7], [10], [13]] -- result for each pair ordered.

    def test_parallel_huge_data_config(self):
        input_list = [[1, 2], [3, 4], [5, 5], [6, str(7) + '1']]  # error in final input
        list_of_results_for_all_pairs = tfrq(sum, input_list)
        print(list_of_results_for_all_pairs)  # [[3], [7], [10], []] -- result for each pair ordered.

        input_list = [[1, 2], [3, 4], [5, 5], [6, str(7) + '1']]  # error in final input
        list_of_results_for_all_pairs = tfrq(sum, input_list, config={"print_errors": True})
        # unsupported operand type(s) for +: 'int' and 'str'
        print(list_of_results_for_all_pairs)  # [[3], [7], [10], []] -- result for each pair ordered.

        input_list = [[1, 2], [3, 4], [5, 5], [6, str(7) + '1']]  # error in final input
        list_of_results_for_all_pairs, errors = tfrq(sum, input_list,
                                                     config={"print_errors": True, "return_errors": True})
        # unsupported operand type(s) for +: 'int' and 'str'
        print(list_of_results_for_all_pairs)  # [[3], [7], [10], []] -- result for each pair ordered.
        print(errors)  # [[], [], [], [TypeError("unsupported operand type(s) for +: 'int' and 'str'")]]

    def test_generator(self):
        numbers = list(range(10))

        for result in tfrq_generator(square, numbers):
            print('res', result)

        params = [(2, 3), (4, 5), (6, 7)]  # Each tuple will be unpacked and passed as arguments to `multiply`
        for result in tfrq_generator(multiply, params, operator="*"):
            print(result)

        params = [{"name": "Alice", "greeting": "Hi"}, {"name": "Bob", "greeting": "Hey"}]
        for result in tfrq_generator(greet, params, operator="**"):
            print(result)


if __name__ == '__main__':
    unittest.main()
