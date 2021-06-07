from global_func import power2, sqrt

# default data for Dots
default_data = {
    "left": None,
    "right": None,
    "top": None,
    "bottom": None,
    "front": None,
    "back": None,
    "name": None,
    "x": -99,
    "y": -99,
    "z": -99,
}


# CLASSES


class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to_center(self, center):
        distance2 = power2(center.x - self.x) + power2(center.y - self.y)
        return sqrt(distance2)

    def __str__(self):
        return f"<{self.x},{self.y},{self.z}>"


class Dot:
    # partisi titik untuk FDM
    def __init__(self, data=default_data):
        self.left = data["left"]
        self.right = data["right"]
        self.top = data["top"]
        self.bottom = data["bottom"]
        self.front = data["front"]
        self.back = data["back"]

        self.name = data["name"]
        self.potential = 0  # akan diisi untuk mencari kapasitansi
        self.coordinate = Coordinate(data["x"], data["y"], data["z"])

    def is_outside(self, center, perimeter):
        return self.coordinate.distance_to_center(center) > perimeter

    def __str__(self):
        return f"{self.name} - {self.coordinate}"