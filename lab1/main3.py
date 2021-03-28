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

polygon = [
    numpy.array([50, 50]),
    numpy.array([100, 150]),
    numpy.array([150, 150]),
    numpy.array([250, 50]),
    numpy.array([275, 75]),
]

FONT = pygame.font.Font(None, 20)

EPS = 0.0000001

def isZero(number):
    return numpy.abs(number) <= EPS


def det(p1, p2, p3, p4):
    return numpy.linalg.det(numpy.array([p2 - p1, p4 - p3]))


def dot(p1, p2, p3, p4):
    return numpy.dot(p2 - p1, p4 - p3)


def intersect(p1, p2, p3, p4):
    d1 = det(p1, p2, p1, p4)
    d2 = det(p1, p2, p1, p3)
    d3 = det(p3, p4, p3, p1)
    d4 = det(p3, p4, p3, p2)

    if isZero(d1) and isZero(d2) and isZero(d3) and isZero(d4):
        c1 = dot(p1, p3, p1, p4)
        c2 = dot(p1, p3, p1, p4)
        c3 = dot(p3, p1, p3, p2)
        c4 = dot(p4, p1, p4, p2)
        if c1 < 0 or c2 < 0 or c3 < 0 or c4 < 0:
            print("collinear intersect")
            return True
        else:
            return False
    else:
        if d1 * d2 < 0 and d3 * d4 < 0:
            print("intersect")
            return True
        else:
            return False


def renderText(sc, message, p):
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))


def next(i):
    return (i + 1) % len(polygon)


complex = False
for i in range(len(polygon)):
    if complex:
        break
    for j in range(i + 1, len(polygon)):
        if complex:
            break
        if intersect(polygon[i], polygon[next(i)], polygon[j], polygon[next(j)]):
            complex = True

if complex:
    print("Complex")
else:
    print("Is not complex")

while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)

    # Draw
    for i in range(len(polygon)):
        pygame.draw.circle(sc, BLACK, polygon[i].tolist(), RADIUS)
        renderText(sc, "p" + str(i), polygon[i])
        pygame.draw.line(sc, BLACK, polygon[i].tolist(), polygon[next(i)].tolist())

    pygame.display.update()

    clock.tick(FPS)
