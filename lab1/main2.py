import pygame
import sys
import numpy

pygame.init()

FPS = 60
WIN_WIDTH = 600
WIN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUNNING = True

RADIUS = 4

clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

p1 = numpy.array([25, 25])
p2 = numpy.array([50, 50])
p3 = numpy.array([50, 50])
p4 = numpy.array([100, 100])

FONT = pygame.font.Font(None, 20)

EPS = 0.0000001

def isZero(number):
    return numpy.abs(number) <= EPS


def det(p1, p2, p3, p4):
    return numpy.linalg.det(numpy.array([p2 - p1, p4 - p3]))


def dot(p1, p2, p3, p4):
    return numpy.dot(p2 - p1, p4 - p3)


d1 = det(p1, p2, p1, p4)
d2 = det(p1, p2, p1, p3)
d3 = det(p3, p4, p3, p1)
d4 = det(p3, p4, p3, p2)

if isZero(d1) and isZero(d2) and isZero(d3) and isZero(d4):
    c1 = dot(p1, p3, p1, p4)
    c2 = dot(p1, p3, p1, p4)
    c3 = dot(p3, p1, p3, p2)
    c4 = dot(p4, p1, p4, p2)
    if c1 <= 0 or c2 <= 0 or c3 <= 0 or c4 <= 0:
        print("collinear Intersect")
    else:
        print("collinear Do not intersect")
else:
    if d1 * d2 <= 0 and d3 * d4 <= 0:
        print("Intersect")
    else:
        print("Do not intersect")


def renderText(sc, message, p):
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))

while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)

    # Draw
    pygame.draw.circle(sc, BLACK, p1.tolist(), RADIUS)
    pygame.draw.circle(sc, BLACK, p2.tolist(), RADIUS)
    pygame.draw.circle(sc, BLACK, p3.tolist(), RADIUS)
    pygame.draw.circle(sc, BLACK, p4.tolist(), RADIUS)
    pygame.draw.line(sc, BLACK, p1.tolist(), p2.tolist())
    pygame.draw.line(sc, BLACK, p3.tolist(), p4.tolist())

    renderText(sc, "p1", p1)
    renderText(sc, "p2", p2)
    renderText(sc, "p3", p3)
    renderText(sc, "p4", p4)

    pygame.display.update()

    clock.tick(FPS)
