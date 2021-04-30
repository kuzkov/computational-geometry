import random
WIN_HEIGHT = 600


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_list(self):
        return [self.x, WIN_HEIGHT - self.y]

    def show(self):
        print("(", self.x, " ", self.y, ")", " ")

    @staticmethod
    def equals(first, second) -> bool:
        return first.x == second.x and first.y == second.y

    @staticmethod
    def generate_random_point(min_x, max_x, min_y, max_y):
        return Point(random.randint(min_x, max_x), random.randint(min_y, max_y))
