import numpy as np

def vector_lengths(arr):
    b = arr ** 2
    b = b.sum(axis = 1)
    b = np.sqrt(b)
    return (b)

a = np.array([[5, 0, 3, 3],
 [7, 9, 3, 5],
 [2, 4, 7, 6],
 [8, 8, 1, 6]])
print(vector_lengths(a))
