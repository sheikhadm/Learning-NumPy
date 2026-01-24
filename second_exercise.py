import numpy as np

def get_row_vectors(input_array):
    row_vectors = []
    row ,column = input_array.shape
    for x in input_array:
        row_vectors.append(x)
    row_vectors = np.array(row_vectors).reshape(1,column)
    return list(row_vectors)

def get_columns_vectors(input_array):
    column_vectors = []
    row ,column = input_array.shape
    parts = np.split(input_array,column,axis = 1)
    # for x in input_array:
    #     column_vectors.append(x)
    # column_vectors = np.array(column_vectors).reshape(row,1)
    return parts

a = np.array([[5, 0, 3],
              [3, 7, 9]])

print(get_columns_vectors(a))