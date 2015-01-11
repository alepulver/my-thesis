from nose.tools import assert_equals
from vector import Vect2D


class Vect2DTest:
    def test_addition(self):
        v1 = Vect2D(1, 2)
        v2 = Vect2D(5, 10)
        v3 = v1 + v2
        assert_equals(v3.x, 6)
        assert_equals(v3.y, 12)

    def test_subtraction(self):
        v1 = Vect2D(1, 2)
        v2 = Vect2D(1, 3)
        v3 = v1 - v2
        assert_equals(v3.x, 0)
        assert_equals(v3.y, -1)

    def test_angle(self):
        v1 = Vect2D(0, 1)
        assert_equals(v1.angle(), 90)

    def test_length(self):
        v1 = Vect2D(3, 4)
        assert_equals(v1.length(), 5)

    def test_dotProd(self):
        v1 = Vect2D(1, 2)
        v2 = Vect2D(2, 3)
        assert_equals(v1.dotProd(v2), 8)

    def test_angleBetween(self):
        v1 = Vect2D(0, 1)
        v2 = Vect2D(1, 1)
        assert_equals(v1.angleBetween(v2), 45)
