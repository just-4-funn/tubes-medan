import numpy as np

from classes import Coordinate, Dot, default_data
from functions import (
    generate_partitions,
    generate_left_matrix,
    generate_right_matrix,
    get_q,
)
from global_func import inv

# Menyusun partisi
partitions = generate_partitions()
# for part in partitions:
#     print(part)
left_mtx = generate_left_matrix(partitions)
right_mtx = generate_right_matrix(partitions)

# Menghitung distribusi potensial

left_mtx = np.array(left_mtx)
right_mtx = np.array(right_mtx)

potential_dist = inv(left_mtx) @ right_mtx

for i in potential_dist:
    print(i)

# Menghitung kapasitansi
q = get_q(potential_dist, partitions)
capacitance = abs(q)  # sebenarnya q/V, tapi V = 1V
print(capacitance)
