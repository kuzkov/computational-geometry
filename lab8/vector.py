import numpy as np


class Vector:
    def __init__(self, x, y=None):
        if y == None:
            vec = x
            if isinstance(vec, Vector):
                self.x = vec.x
                self.y = vec.y
            else:
                self.x = vec[0]
                self.y = vec[1]
        else:
            self.x = x
            self.y = y

    def add(self, x, y=None):
        if y == None:
            self.x += x.x
            self.y += x.y
            return self

        self.x += x
        self.y += y
        return self

    def get_right_normal(self):
        return Vector(self.y, -self.x)

    def get_left_normal(self):
        return Vector(-self.y, self.x)

    @classmethod
    def mult(cls, v, k):
        return Vector(v.x * k, v.y * k)

    @classmethod
    def add(cls, vec1, vec2):
        return Vector(vec1.x + vec2.x, vec1.y + vec2.y)

    @classmethod
    def subtract(cls, vec1, vec2):
        return Vector(vec1.x - vec2.x, vec1.y - vec2.y)

    @classmethod
    def dot(cls, vec1, vec2):
        return vec1.x * vec2.x + vec1.y * vec2.y

    def as_array(self):
        return [self.x, self.y]

    def is_equal_to(self, vector):
        return self.x == vector.x and self.y == vector.y