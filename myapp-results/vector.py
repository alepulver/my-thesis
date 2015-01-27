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
        radians = math.atan2(self.y, self.x)
        return math.degrees(radians)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angleBetween(self, other):
        m1 = self.length()
        m2 = other.length()
        if m1 == 0:
            return other.angle()
        elif m2 == 0:
            return self.angle()

        if self.x == other.x and self.y == other.y:
            return 0

        #radians = math.acos(self.dotProd(other) / (m1 * m2))
        radians = math.atan2(other.y, other.x) - math.atan2(self.y, self.x)

        return math.degrees(radians)

    def dotProd(self, other):
        return self.x * other.x + self.y * other.y
