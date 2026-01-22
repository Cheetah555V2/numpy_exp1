import numpy as np

#basically 2d array
arr = np.array([[1, 2, 3, 4, 5, 6, 7],
                [8, 9, 10, 11, 12, 13, 14]])

# [1 2 3 4 5 6 7]
print(arr[0])

# From all rows, return the third element
# [3 10]
print(arr[:,2])

# From all rows, return the 0, 2, 4 elements
# [[ 1  3  5]
#  [ 8 10 12]]
print(arr[:,0:5:2])

#Which if we use this on list, it will give us an error
try:
    l = [[1, 2, 3, 4, 5, 6, 7],[8, 9, 10, 11, 12, 13, 14]]
    print(l[:,2])
except:
    print("Oh no we got error")