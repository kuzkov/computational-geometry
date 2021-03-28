from segment import Segment
from polygon import Polygon


class ConvexPolygon(Polygon):
    # TODO: Override constructor to determine if a polygon is convex and counterclockwise

    # Only counterclockwise
    def contains(self, point):
        n = len(self.points)
        if point.direction(Segment(self.points[0], self.points[1])) < 0 or point.direction(
                Segment(self.points[0], self.points[n - 1])) > 0:
            return False

        p, r = 1, n - 1
        while r - p > 1:
            q = (p + r) // 2
            if point.direction(Segment(self.points[0], self.points[q])) < 0:
                r = q
            else:
                p = q

        return not Segment(self.points[0], point).intersects(Segment(self.points[p], self.points[r]))
