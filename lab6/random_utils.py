from random import uniform
from point import Point


def generate_random_points(count, min_x, max_x, min_y, max_y):
    return [
        Point(
            uniform(min_x, max_x),
            uniform(min_y, max_y)
        ) for _ in range(count)
    ]
