from classes import Coordinate

# pas testing pake partisi 1cm (0.01) makan waktu hampir semenit
# klo mau coba2 bisa pake partisi lebih gede biar waktu nunggunya manusiawi

# Editable
perimeter = 0.1
height = 0.1
partition_length = 0.02  # 0.01, 0.02, atau 0.025
center_coordinate = Coordinate(0.1, 0.1, 0.05)

# Initial variables
diameter = perimeter * 2
ver_parts = int(height // partition_length) - 1  # jumlah partisi vertikal
hor_parts = int(diameter // partition_length) - 1  # jumlah partisi horizontal

# Const
epsilon = 8.85418782 * (10 ** -12)