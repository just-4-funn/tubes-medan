from classes import Coordinate
from global_func import power2

# Editable
perimeter = 0.1
height = 0.1
partition_length = 0.01
center_coordinate = Coordinate(0.1, 0.1, 0.05)

# Initial variables
diameter = perimeter * 2
num_of_part_per_side = int(diameter // partition_length)
num_of_part_per_shape = power2(num_of_part_per_side)
num_of_partitions = num_of_part_per_shape * 2

# const
epsilon = 8.85418782 * (10 ** -12)


# Buat bagian FDM
ver_parts = int(height // partition_length) - 1  # jumlah partisi vertikal
hor_parts = int(diameter // partition_length) - 1  # jumlah partisi horizontal