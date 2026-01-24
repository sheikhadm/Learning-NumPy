import numpy as np

def multiplication_table(n:int):
    arr = np.arange(n)
    arr_j = np.arange(n).reshape((n,1))
    print(arr*arr_j)

multiplication_table(4)
