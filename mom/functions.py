import math
from global_func import power2, sqrt, inv
from classes import Partition, Coordinate
from variables import (
    perimeter,
    diameter,
    height,
    partition_length,
    center_coordinate,
    num_of_part_per_side,
    num_of_part_per_shape,
    num_of_partitions,
    ver_parts,
    hor_parts,
    epsilon,
)

# FOR ANOTHER FUNCTIONS


def handle_self():
    res = (2 * sqrt(math.pi)) / partition_length
    return res


def handle_other(part1, part2):
    return 1 / part1.distance_to_coordinate(part2.center)


def get_coordinate(i):
    x = (
        (i // num_of_part_per_side) % num_of_part_per_shape * partition_length
    ) % diameter
    y = (i % num_of_part_per_shape) % num_of_part_per_side * partition_length
    z = 0 if i >= num_of_part_per_shape else height
    return (x, y, z)


# FOR main.py


def get_partitions():
    partitions = []

    for i in range(num_of_partitions):
        (x, y, z) = get_coordinate(i)
        x += partition_length / 2
        y += partition_length / 2
        partition = Partition(i, x, y, z)
        if not partition.is_outside(center_coordinate, perimeter):
            partitions.append(partition)

    return partitions


def get_left_matrix(partitions):
    num_of_partitions = len(partitions)
    matrix = [[0 for i in range(num_of_partitions)] for j in range(num_of_partitions)]

    def is_invalid(i, j):
        return (
            partitions[j].distance_to_center(center_coordinate) > perimeter
            or partitions[i].distance_to_center(center_coordinate) > perimeter
        )

    for i in range(num_of_partitions):
        for j in range(num_of_partitions):
            if is_invalid(i, j):
                continue
            if i == j:
                matrix[i][j] = handle_self()
            else:
                matrix[i][j] = handle_other(partitions[i], partitions[j])

    return matrix


def get_right_matrix(val, partitions):
    right_mtx = []
    part_count = len(partitions)
    half = part_count // 2

    for i in range(part_count):
        if partitions[i].is_outside(center_coordinate, perimeter):
            right_mtx.append(0)
        elif i < half:
            right_mtx.append(val)
        else:
            right_mtx.append(-1 * val)

    return right_mtx


def get_Q(mtx, partition_area):
    q_sum = 0
    for i in range(len(mtx)):
        q_sum += mtx[i] * partition_area
    return q_sum


def get_fdm_partitions():
    partitions = []

    for i in range(ver_parts):
        for j in range(hor_parts):
            for k in range(hor_parts):
                x = partition_length * (j + 1)
                y = partition_length * (k + 1)
                z = partition_length * (ver_parts - i)
                partition = Coordinate(x, y, z)
                if partition.distance_to_center(center_coordinate) < perimeter:
                    partitions.append(partition)

    return partitions


def get_potential_dist(fdm_parts, mom_parts, res_mtx, partition_area):
    mtx = []
    for i in range(len(fdm_parts)):
        total = 0
        for j in range(len(mom_parts)):

            Q = res_mtx[j] * partition_area
            delta_r = mom_parts[j].distance_to_coordinate(fdm_parts[i])
            total += Q / delta_r
        potential = total / (4 * math.pi * epsilon)
        mtx.append(potential)
    return mtx
