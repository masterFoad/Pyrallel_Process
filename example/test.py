import unittest

from tfrq import tfrq


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
        list_of_results_for_all_pairs = tfrq(sum, input_list)
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


if __name__ == '__main__':
    unittest.main()
