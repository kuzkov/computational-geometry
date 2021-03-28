import pygame
import sys
import math

from convex_polygon import ConvexPolygon
from segment import Segment
from polygon import Polygon
from point import Point
from vector import Vector
from random_utils import *


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

COUNT_OF_POINTS = 150
points = generate_random_points(COUNT_OF_POINTS, 0, WIN_WIDTH, 0, WIN_HEIGHT)
polygon_coords = [
    Point(600, 453),
    Point(414, 497),
    Point(196, 446),
    Point(62, 325),
    Point(45, 84),
    Point(140, 48),
    Point(548, 43),
]
inner_polygon_coords = [
    Point(469, 349),
    Point(381, 246),
    Point(300, 293),
    Point(217, 280),
    Point(214, 215),
    Point(288, 198),
    Point(445, 207),
]
polygon = ConvexPolygon(polygon_coords)
inner_polygon = Polygon(inner_polygon_coords)


def next(n, i):
    return (i + n) % n


def render_text(sc, message, p):
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))


points = list(filter(lambda point: polygon.contains(point), points))
points = list(filter(lambda point: not inner_polygon.contains(point), points))

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

    # Draw polygon
    for index, point in enumerate(polygon_coords, start=1):
        pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)
        pygame.draw.line(sc, BLACK, point.tolist(), polygon_coords[next(len(polygon_coords), index)].tolist(), 1)
    pygame.draw.line(sc, BLACK, polygon_coords[len(polygon_coords) - 1].tolist(), polygon_coords[0].tolist(), 1)

    # Draw inner polygon
    for index, point in enumerate(inner_polygon_coords, start=1):
        pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)
        pygame.draw.line(sc, BLACK, point.tolist(), inner_polygon_coords[next(len(inner_polygon_coords), index)].tolist(), 1)
    pygame.draw.line(sc, BLACK, polygon_coords[len(inner_polygon_coords) - 1].tolist(), polygon_coords[0].tolist(), 1)


    pygame.display.update()

    n = len(polygon_coords)
    # Update
    for i, point in enumerate(points):
        if inner_polygon.contains(point):
            velocity_vectors[i] = Vector(0, 0)

        if not point.within_polygon(polygon):
            for j in range(n):
                segment = Segment(polygon_coords[j], polygon_coords[(j + 1) % n])
                if point.direction(Segment(polygon_coords[j], polygon_coords[(j + 1) % n])) < 0:
                    velocity_vectors[i].reflect(segment.as_vector())

        points[i].add(velocity_vectors[i])

    clock.tick(FPS)
