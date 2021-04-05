import numpy as np


class Vector:
    def __init__(self, x, y=None):
        if y is None:
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
        if y is None:
            self.x += x.x
            self.y += x.y
            return self

        self.x += x
        self.y += y
        return self

    @classmethod
    def subtract(cls, vec1, vec2):
        return Vector(vec1.x - vec2.x, vec1.y - vec2.y)

    @classmethod
    def subtract(cls, vec1, vec2):
        return Vector(vec1.x - vec2.x, vec1.y - vec2.y)

    def tolist(self):
        return [self.x, self.y]

    def as_array(self):
        return [self.x, self.y]

    def is_equal_to(self, vector):
        return self.x == vector.x and self.y == vector.y

    def reflect(self, vector):
        a = np.array([self.x, self.y])
        b = np.array([vector.x, vector.y])
        res = 2 * (np.dot(a, b) / np.dot(b, b)) * b - a

        self.x = res[0]
        self.y = res[1]
        return self
