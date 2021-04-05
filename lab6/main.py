import pygame
import sys
import math

from convex_polygon import ConvexPolygon
from segment import Segment
from polygon import Polygon
from vector import Vector
from random_utils import *
from set import Set


pygame.init()

FPS = 60
WIN_WIDTH = 700
WIN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUNNING = True

RADIUS = 4

clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FONT = pygame.font.Font(None, 20)

OFFSET = 325
COUNT_OF_POINTS = 20
points = generate_random_points(COUNT_OF_POINTS, OFFSET, WIN_WIDTH - OFFSET, OFFSET, WIN_HEIGHT - OFFSET)
MAX_PERIMETER = 500


def render_text(sc, message, p):
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))


velocity = 1
velocity_vectors = [Vector(velocity * math.cos(uniform(0, 2 * math.pi)), velocity * math.sin(uniform(0, 2 * math.pi))) for _ in points]


while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)

    # Draw
    for index, point in enumerate(points, start=1):
        pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)

    # # Draw polygon
    # for index, point in enumerate(polygon_coords, start=1):
    #     pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)
    #     pygame.draw.line(sc, BLACK, point.tolist(), polygon_coords[next(len(polygon_coords), index)].tolist(), 1)
    # pygame.draw.line(sc, BLACK, polygon_coords[len(polygon_coords) - 1].tolist(), polygon_coords[0].tolist(), 1)
    #
    # # Draw inner polygon
    # for index, point in enumerate(inner_polygon_coords, start=1):
    #     pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)
    #     pygame.draw.line(sc, BLACK, point.tolist(), inner_polygon_coords[next(len(inner_polygon_coords), index)].tolist(), 1)
    # pygame.draw.line(sc, BLACK, polygon_coords[len(inner_polygon_coords) - 1].tolist(), polygon_coords[0].tolist(), 1)


    pygame.display.update()

    convex = Set(points).quick_hull()
    perimeter = convex.perimeter()

    if perimeter > MAX_PERIMETER:
        for vector in velocity_vectors:
            vector.x *= -1
            vector.y *= -1

    # Update
    for i, point in enumerate(points):
        points[i].add(velocity_vectors[i])

    clock.tick(FPS)
