import math
import numpy as np
from vector import Vector
import point

class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1 if isinstance(p1, point.Point) else point.Point(p1)
        self.p2 = p2 if isinstance(p2, point.Point) else point.Point(p2)

    def is_collinear_to(self, segment):
        v1 = segment.as_vector()
        v2 = self.as_vector()

        return math.isclose(v1.x * v2.y - v1.y * v2.x, 0)

    def equal(self, segment):
        return self.p1.x == segment.p1.x and self.p1.y == segment.p1.y and self.p2.x == segment.p2.x and self.p2.y == segment.p2.y

    def as_vector(self):
        return Vector(self.p2.x - self.p1.x, self.p2.y - self.p1.y)

    def length(self):
        return math.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

    def aimAt(self, segment):
        qv = self.as_vector()
        pv = segment.as_vector()
        cross = pv.x * qv.y - pv.y * qv.x

        inside_half_plane = self.p2.direction(segment) >= 0

        if inside_half_plane:
            return cross < 0
        else:
            return cross >= 0

    def intersection(self, segment):
        xdiff = (self.p1.x - self.p2.x, segment.p1.x - segment.p2.x)
        ydiff = (self.p1.y - self.p2.y, segment.p1.y - segment.p2.y)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('Lines do not intersect')

        d = (det((self.p1.x, self.p1.y), (self.p2.x, self.p2.y)),
             det((segment.p1.x, segment.p1.y), (segment.p2.x, segment.p2.y)))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        return point.Point(x, y)

    def is_inside(self, segment):  # returns True if self is inside segment
        return self.p1.direction(segment) <= 0 and self.p2.direction(segment) <= 0

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


