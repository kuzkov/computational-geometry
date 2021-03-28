import math
import numpy as np
from vector import Vector
from segment import Segment


class Point(Vector):
    def direction(self, segment):
        det = np.linalg.det([
            segment.as_vector().as_array(),
            Segment(segment.p1, self).as_vector().as_array()
        ])
        return 1 if det > 0 else 0 if math.isclose(det, 0) else -1

    def inside_segment(self, segment):
        pass

    def within_polygon(self, polygon):
        return polygon.contains(self)
