import math


class Vect2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect2D(self.x - other.x, self.y - other.y)

    def angle(self):
        return math.atan2(self.y, self.x)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angleBetween(self, other):
        radians = math.acos(self.dotProd(other) / (self.length() * other.length()))
        return math.degrees(radians)

    def dotProd(self, other):
        return self.x * other.x + self.y * other.y
