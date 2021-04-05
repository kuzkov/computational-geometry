import math
from polygon import Polygon
from segment import Segment


class Set:
    def __init__(self, points):
        self.points = points

    def quick_hull(self):
        if len(self.points) < 3:
            return self.points

        result = []

        extremes = self.__get_extremes(self.points)

        self.__add_farthest(self.points, extremes['left'], extremes['right'], result)
        self.__add_farthest(self.points, extremes['right'], extremes['left'], result)

        return Polygon(self.__sort(result, extremes['left']))

    def __get_extremes(self, points):
        left = points[0]
        right = points[0]

        for point in points[1:]:
            if left.x > point.x:
                left = point
            if right.x < point.x:
                right = point

        return {
            'left': left,
            'right': right
        }

    def __add_farthest(self, points, left, right, result):
        farthest = None
        max_area = 0

        for point in points:
            if point.direction(Segment(left, right)) > 0:  # on the left
                area = self.__area(left, right, point)
                if area > max_area:
                    farthest = point
                    max_area = area

        if farthest is None:
            self.__add_extremes(left, right, result)
            return

        self.__add_farthest(points, left, farthest, result)
        self.__add_farthest(points, farthest, right, result)

    def __add_extremes(self, p1, p2, points):
        if p1 not in points:
            points.append(p1)
        if p2 not in points:
            points.append(p2)

    def __area(self, p1, p2, p):
        return abs((p.y - p1.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p.x - p1.x))

    def __sort(self, points, init_point):
        points.remove(init_point)
        angles = list(map(lambda p: math.atan2(p.y - init_point.y, p.x - init_point.x), points))
        return [init_point] + [p for _, p in sorted(zip(angles, points))]