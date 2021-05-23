import random
import numpy as np

from constants import WIN_HEIGHT
from constants import WIN_WIDTH
from constants import HORIZONTAL_BORDER_SPACING
from constants import VERTICAL_BORDER_SPACING
from constants import RADIUS

class Circle:
    def __init__(self, x, y, radius, velocity_vector):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_vector = velocity_vector

    def to_list(self):
        return [self.x, WIN_HEIGHT - self.y]

    def show(self):
        print("(", self.x, " ", self.y, ")", " ")

    def move(self):
        self.x += self.velocity_vector[0]
        self.y += self.velocity_vector[1]

    def get_velocity_vector(self):
        return self.velocity_vector

    def border_strike(self):
        if self.x - self.radius + self.velocity_vector[0] <= HORIZONTAL_BORDER_SPACING:
            self.x = HORIZONTAL_BORDER_SPACING + self.radius
            self.reflect([0, 1])
        if self.x + self.radius + self.velocity_vector[0] >= WIN_WIDTH - HORIZONTAL_BORDER_SPACING:
            self.x = WIN_WIDTH - HORIZONTAL_BORDER_SPACING - self.radius
            self.reflect([0, 1])
        if self.y - self.radius + self.velocity_vector[1] <= VERTICAL_BORDER_SPACING:
            self.y = VERTICAL_BORDER_SPACING + self.radius
            self.reflect([1, 0])
        if self.y + self.radius + self.velocity_vector[1] >= WIN_HEIGHT - VERTICAL_BORDER_SPACING:
            self.y = WIN_HEIGHT - VERTICAL_BORDER_SPACING - self.radius
            self.reflect([1, 0])

    def reflect(self, vector):
        a = np.array([self.velocity_vector[0], self.velocity_vector[1]])
        b = np.array([vector[0], vector[1]])
        res = 2 * (np.dot(a, b) / np.dot(b, b)) * b - a

        self.velocity_vector[0] = res[0]
        self.velocity_vector[1] = res[1]

    def reverse_velocity_vector(self):
        self.velocity_vector[0], self.velocity_vector[1] = -self.velocity_vector[0], -self.velocity_vector[1]

    @staticmethod
    def equals(first, second) -> bool:
        return (
            first.x == second.x
            and first.y == second.y
            and first.velocity_vector[0] == second.velocity_vector[0]
            and first.velocity_vector[1] == second.velocity_vector[1]
            and first.radius == second.radius
        )

    @staticmethod
    def find_distance_between_centers(first, second):
        return ((first.x - second.x) ** 2 + (first.y - second.y) ** 2) ** (1 / 2)

    @staticmethod
    def generate_random_circle(min_x, max_x, min_y, max_y, x_velocity_vector_limit, y_velocity_vector_limit):
        return Circle(random.randint(min_x, max_x), random.randint(min_y, max_y), RADIUS,
                          [random.randint(1, x_velocity_vector_limit) * ((-1) ** random.randint(1, 2)),
                           random.randint(1, y_velocity_vector_limit) * ((-1) ** random.randint(1, 2))]
        )
