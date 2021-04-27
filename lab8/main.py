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
BLUE = (50, 50, 255)
RED = (255, 50, 50)
RUNNING = True

RADIUS = 4

clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FONT = pygame.font.Font(None, 20)

P = ConvexPolygon([
    (150, 350),
    (300, 250),
    (300, 150),
    (200, 100),
    (100, 200)
])

Q = ConvexPolygon([
    (600, 600),
    (650, 450),
    (600, 350),
    (500, 450),
    (450, 600)
])

def render_text(sc, message, p):
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))

def next(n, i):
    return (i + 1) % n

while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)

    # Update
    for i in range(len(P.points)):
        P.points[i].x += 1.2
        P.points[i].y += 0.8

    for i in range(len(Q.points)):
        Q.points[i].x -= 0.8
        Q.points[i].y -= 1.2

    R = P.clip_polygon(Q)

    # Drap segment

    segment = Segment(P.points[2], P.points[0])
    pygame.draw.line(sc, BLACK, P.points[2].tolist(), P.points[0].tolist(), 1)

    # Draw P
    for index, point in enumerate(P.points):
        render_text(sc, "p" + str(index), point.tolist())
        pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)
        pygame.draw.line(sc, BLACK, point.tolist(), P.points[next(len(P.points), index)].tolist(), 1)
    pygame.draw.line(sc, BLACK, P.points[len(P.points) - 1].tolist(), P.points[0].tolist(), 1)

    # Draw Q
    for index, point in enumerate(Q.points):
        render_text(sc, "q" + str(index), point.tolist())
        pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)
        pygame.draw.line(sc, BLACK, point.tolist(), Q.points[next(len(Q.points), index)].tolist(), 1)
    pygame.draw.line(sc, BLACK, Q.points[len(Q.points) - 1].tolist(), Q.points[0].tolist(), 1)

    if len(R.points) > 1:
        pygame.draw.polygon(sc, RED, list(map(lambda point: point.tolist(), R.points)))

    clipped_segment = Q.clip_segment(segment)

    if clipped_segment is not None:
        pygame.draw.line(sc, BLUE, clipped_segment.p1.tolist(), clipped_segment.p2.tolist(), 5)

    pygame.display.update()

    clock.tick(FPS)
