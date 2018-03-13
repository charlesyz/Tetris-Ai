import numpy as np


input = [[1,2,3],[4,5,6]]

a = np.array(input).flatten()

a = np.append(a, [1]).reshape(7z, 1)

print(a)