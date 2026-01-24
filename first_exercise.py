import numpy as np

def get_rows(two_dimensional_array):
    row_list = []
    for x in two_dimensional_array:
        row_list.append(x)
    return row_list

def get_columns(two_dimensional_array):
    new_list = two_dimensional_array.T
    row_list = []
    for x in new_list:
        row_list.append(x)
    return row_list

a = np.array([[5, 0, 3, 3],
 [7, 9, 3, 5],
 [2, 4, 7, 6],
 [8, 8, 1, 6]])
print(get_columns(a))