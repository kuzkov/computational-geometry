from vector import Vector
from segment import Segment
from point import Point


class Polygon:
    # Only counterclockwise
    def __init__(self, points):
        self.points = list(map(lambda point: point if isinstance(point, Point) else Point(point), points))

    def contains(self, point):
        def get_octant(vector):
            x = vector.x
            y = vector.y

            if x == 0 and y == 0:
                return 0
            if 0 <= y < x:
                return 1
            if 0 < x <= y:
                return 2
            if -y <= x <= 0:
                return 3
            if 0 < y <= -x:
                return 4
            if x < y <= 0:
                return 5
            if y <= x < 0:
                return 6
            if 0 <= x < -y:
                return 7
            if -x <= y < 0:
                return 8

        n = len(self.points)

        def next(i):
            return (i + 1) % n

        s = d = 0

        for i in range(n):
            if point.is_equal_to(self.points[i]):
                return True

            o1 = get_octant(Vector.subtract(self.points[i], point))
            o2 = get_octant(Vector.subtract(self.points[next(i)], point))
            d = o2 - o1

            if d > 4:
                d -= 8
            elif d < -4:
                d += 8
            elif d == 4 or d == -4:
                segment = Segment(self.points[i], self.points[next(i)])
                if point.direction(segment) < 0:  # right
                    d = -4
                elif point.direction(segment) > 0:  # left
                    d = 4
                else:
                    return True

            s += d

        if s == 0:
            return False
        elif s == 8 or s == -8:
            return True

        print("wtf")
