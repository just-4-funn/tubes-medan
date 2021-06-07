# Python Libraries
import math
import numpy as np

# Import from other files
from variables import partition_length, epsilon
from global_func import power2, inv
from functions import (
    get_right_matrix,
    get_partitions,
    get_left_matrix,
    get_Q,
    get_fdm_partitions,
    get_potential_dist,
)

# mencari rho s
partitions = get_partitions()
left_mtx = get_left_matrix(partitions)
left_mtx = np.array(left_mtx)

right_val = (4 * math.pi * epsilon) / (power2(partition_length))
right_mtx = get_right_matrix(right_val, partitions)
right_mtx = np.array(right_mtx)

result_mtx = inv(left_mtx) @ right_mtx

# mencari kapasitansi
partition_area = power2(partition_length)
voltage_diff = 2  # beda potensial 1-(-1)
capacitance = abs(get_Q(result_mtx, partition_area) / voltage_diff)
# print(capacitance)

# mencari distribusi potensial
fdm_partitions = get_fdm_partitions()
potential_dist = get_potential_dist(
    fdm_partitions, partitions, result_mtx, partition_area
)
print(potential_dist)