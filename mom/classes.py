from global_func import power2, sqrt

# CLASSES


class Coordinate:
    def __init__(self, x, y, z):
        # default value andai x,y,z ga dimasukin
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"<{self.x},{self.y},{self.z}>"

    def distance_to_center(self, center):
        distance2 = power2(center.x - self.x) + power2(center.y - self.y)
        return sqrt(distance2)


class Partition:  # Partisi 2D buat MOM
    def __init__(self, name, x, y, z):
        self.name = name
        self.center = Coordinate(x, y, z)

    def distance_to_center(self, center):
        return self.center.distance_to_center(center)

    def is_outside(self, center, perimeter):
        return self.distance_to_center(center) > perimeter

    def distance_to_coordinate(self, coordinate):
        (x, y, z) = (coordinate.x, coordinate.y, coordinate.z)
        distance2 = (
            power2(x - self.center.x)
            + power2(y - self.center.y)
            + power2(z - self.center.z)
        )
        return sqrt(distance2)

    def __str__(self):
        return f"{self.name} - {self.center}"
