import math
import numpy as np
from vector import Vector


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1 if isinstance(p1, Vector) else Vector(p1)
        self.p2 = p2 if isinstance(p2, Vector) else Vector(p2)

    def as_vector(self):
        return Vector(self.p2.x - self.p1.x, self.p2.y - self.p1.y)

    def length(self):
        return math.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

    def intersects(self, segment):
        if segment.p1.is_equal_to(self.p1) or segment.p2.is_equal_to(self.p2):
            return True

        d1 = np.linalg.det([
            self.as_vector().as_array(),
            Segment(self.p1, segment.p1).as_vector().as_array()
        ])
        d2 = np.linalg.det([
            self.as_vector().as_array(),
            Segment(self.p1, segment.p2).as_vector().as_array()
        ])
        d3 = np.linalg.det([
            segment.as_vector().as_array(),
            Segment(segment.p1, self.p1).as_vector().as_array()
        ])
        d4 = np.linalg.det([
            segment.as_vector().as_array(),
            Segment(segment.p1, self.p2).as_vector().as_array()
        ])

        if math.isclose(d1, 0) and math.isclose(d2, 0) and math.isclose(d3, 0) and math.isclose(d4, 0):
            c1 = np.linalg.dot(
                Segment(self.p1, segment.p1).as_vector().as_array(),
                Segment(self.p1, segment.p2).as_vector().as_array()
            )
            c2 = np.linalg.dot(
                Segment(self.p2, segment.p1).as_vector().as_array(),
                Segment(self.p2, segment.p2).as_vector().as_array()
            )
            c3 = np.linalg.dot(
                Segment(segment.p1, self.p1).as_vector().as_array(),
                Segment(segment.p1, self.p2).as_vector().as_array()
            )
            c4 = np.linalg.dot(
                Segment(segment.p2, self.p1).as_vector().as_array(),
                Segment(segment.p2, self.p2).as_vector().as_array()
            )
            if c1 <= 0 or c2 <= 0 or c3 <= 0 or c4 <= 0:
                return True
            else:
                return False
        else:
            if d1 * d2 <= 0 and d3 * d4 <= 0:
                return True
            else:
                return False
