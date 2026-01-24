import numpy as np

def diamond(n):
    left_side = np.eye(n  , dtype = int)
    new_side = left_side[:,::-1]
    right_side = new_side[:,1:]
    down_side =  np.concatenate((left_side, right_side),axis = 1)
    left_trim = left_side[:,1:]
    top_side = np.concatenate((new_side,left_trim),axis =1)
    down_trim = down_side[1:,:]
    return np.concatenate((top_side,down_trim),axis =0)

print(diamond(6))