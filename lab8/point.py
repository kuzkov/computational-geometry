import math
import numpy as np
from vector import Vector
import segment as segment_lib


class Point(Vector):
    def direction(self, segment):
        det = np.linalg.det([
            segment.as_vector().as_array(),
            segment_lib.Segment(segment.p1, self).as_vector().as_array()
        ])
        return 1 if det > 0 else 0 if math.isclose(det, 0) else -1 # 1 left, -1 right, 0 on

    def inside_segment(self, segment):
        pass

    def tolist(self):
        return (self.x, self.y)

    def within_polygon(self, polygon):
        return polygon.contains(self)
