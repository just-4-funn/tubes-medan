from classes import Coordinate, Dot, default_data
from global_func import power2
from variables import (
    perimeter,
    height,
    partition_length,
    center_coordinate,
    ver_parts,
    hor_parts,
    epsilon,
)

# FOR ANOTHER FUNCTIONS
def init_name_coordinate():
    # mengisi nama dan koordinat semua partisi
    count = 0
    arr = []
    for i in range(ver_parts):
        for j in range(hor_parts):
            for k in range(hor_parts):
                data = {**default_data}
                data["x"] = partition_length * (j + 1)
                data["y"] = partition_length * (k + 1)
                data["z"] = partition_length * (ver_parts - i)
                data["name"] = count

                arr.append(Dot(data))
                count += 1
    return arr


def fill_z_axis(dot, arr):
    # menentukan partisi atas dan bawah partisi
    def is_top():  # sb z+
        # mengecek apakah partisi lapisan paling atas (sb-z)
        return int(dot.name) < power2(hor_parts)

    def is_bottom():  # sb y-
        # mengecek apakah partisi lapisan paling bawah (sb-z)
        return int(dot.name) > power2(hor_parts) * (ver_parts - 1)

    if is_top():
        dot.top = 1  # V atas = 1 V
    else:
        dot.top = arr[int(dot.name) - power2(hor_parts)]

    if is_bottom():
        dot.bottom = -1  # V atas = -1 V
    else:
        dot.bottom = arr[int(dot.name) + power2(hor_parts)]
    return dot


def fill_y_axis(dot, arr):
    (x, y, z) = (dot.coordinate.x, dot.coordinate.y, dot.coordinate.z)

    def is_right():  # sb y+
        right_coordinates = Coordinate(x, y + partition_length, z)
        return right_coordinates.distance_to_center(center_coordinate) >= perimeter

    def is_left():  # sb y-
        left_coordinates = Coordinate(x, y - partition_length, z)
        return left_coordinates.distance_to_center(center_coordinate) >= perimeter

    if not is_right():
        dot.right = arr[int(dot.name) + 1]
    if not is_left():
        dot.left = arr[int(dot.name) - 1]
    return dot


def fill_x_axis(dot, arr):
    (x, y, z) = (dot.coordinate.x, dot.coordinate.y, dot.coordinate.z)

    def is_front():  # sb x-
        front_coordinates = Coordinate(x - partition_length, y, z)
        return front_coordinates.distance_to_center(center_coordinate) >= perimeter

    def is_back():  # sb x+
        back_coordinates = Coordinate(x + partition_length, y, z)
        distance = back_coordinates.distance_to_center(center_coordinate) + 0.00001
        # entah kenapa desimalnya python ga akurat, jadi ditambah 0.00001 biar lebih akurat
        return distance >= perimeter

    if not is_front():
        dot.front = arr[int(dot.name) - hor_parts]
    if not is_back():
        dot.back = arr[int(dot.name) + hor_parts]
    return dot


def fill_neighbors_part(arr):
    # menentukan bagian kanan kiri atas bawah depan belakang dari partisi
    for i in range(len(arr)):
        if arr[i].is_outside(center_coordinate, perimeter):
            continue
        arr[i] = fill_z_axis(arr[i], arr)
        arr[i] = fill_y_axis(arr[i], arr)
        arr[i] = fill_x_axis(arr[i], arr)
    return arr


def fill_self(mtx, length):
    # mengisi bagian dimana i == j (6)
    for i in range(length):
        for j in range(length):
            if i == j:
                mtx[i][j] = 6
    return mtx


def find_index(partitions, name):
    for i in range(len(partitions)):
        if str(partitions[i].name) == str(name):
            return i


def fill_neighbor(mtx, arr):
    # mengisi left_mtx dengan elemen sekitar (1)
    def is_valid(neighbor):
        return isinstance(neighbor, Dot)

    for i in range(len(arr)):
        partition = arr[i]

        if is_valid(partition.top):
            mtx[i][find_index(arr, partition.top.name)] = 1
        if is_valid(partition.bottom):
            mtx[i][find_index(arr, partition.bottom.name)] = 1
        if is_valid(partition.left):
            mtx[i][find_index(arr, partition.left.name)] = 1
        if is_valid(partition.right):
            mtx[i][find_index(arr, partition.right.name)] = 1
        if is_valid(partition.front):
            mtx[i][find_index(arr, partition.front.name)] = 1
        if is_valid(partition.back):
            mtx[i][find_index(arr, partition.back.name)] = 1
    return mtx


def find_partition(arr, i):
    # mencari partisi yang memiliki name == str(i)
    for part in arr:
        if str(part.name) == str(i):
            return part
    return None


# FOR main.py


def generate_partitions():
    arr = init_name_coordinate()
    arr = fill_neighbors_part(arr)
    partitions = []
    for i in range(len(arr)):
        if not arr[i].is_outside(center_coordinate, perimeter):
            partitions.append(arr[i])
    return partitions


def generate_left_matrix(arr):
    length = len(arr)
    mtx = [[0 for i in range(length)] for j in range(length)]
    mtx = fill_self(mtx, length)
    mtx = fill_neighbor(mtx, arr)
    return mtx


def generate_right_matrix(arr):
    mtx = [0 for i in range(len(arr))]
    for i in range(len(arr)):
        if arr[i].top == 1:
            mtx[i] = -1
        if arr[i].bottom == -1:
            mtx[i] = 1
    return mtx


def get_q(arr, partitions):
    # karena di luar tabung potensial = 0 dan tidak ada perbedaan epsilon,
    # maka tinjau permukaan 'kubus' di bawah tabung
    # diambil layer kedua dan ketiga teratas (bebas)
    # karena h1 & h2 sama, jadi bisa dicoret (asumsi epsilon = epsilon_nol)

    # nentuin batas atas sama bawah sample array
    top_start = power2(hor_parts) * 2  # layer 2
    top_end = top_start + power2(hor_parts)
    bottom_start = power2(hor_parts) * 3  # layer 3
    bottom_end = bottom_start + power2(hor_parts)

    # mengisi array partition (berisi Dots) dengan potensial yang sesuai
    for i in range(len(arr)):
        partitions[i].potential = arr[i]

    # ngambil partisi array
    top_layer = arr[top_start:top_end]
    bottom_layer = arr[bottom_start:bottom_end]
    top_layer = []
    bottom_layer = []

    for i in range(top_start, top_end):
        part = find_partition(partitions, i)
        if part:
            top_layer.append(part.potential)
        else:
            top_layer.append(0)

    for i in range(bottom_start, bottom_end):
        part = find_partition(partitions, i)
        if part:
            bottom_layer.append(part.potential)
        else:
            bottom_layer.append(0)

    # perhitungan q
    q = 0
    for i in range(len(top_layer)):
        q += (top_layer[i] - bottom_layer[i]) * epsilon

    # aslinya negatif, jadi dikali -1 lagi
    return -q
