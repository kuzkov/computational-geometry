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
EPS = 0.0000001

clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FONT = pygame.font.Font(None, 20)




def lieInBoardersOfPolinom(dots, p0): #dimensionalTest
    minx = dots[0][0]
    miny = dots[0][1]
    maxx = dots[0][0]
    maxy = dots[0][0]

    for i in dots:
        if i[0] > maxx:
            maxx = i[0]
        if i[0] < minx:
            minx = i[0]
        if i[1] > maxy:
            maxy = i[1]
        if i[1] < miny:
            miny = i[1]

    if minx <= p0[0] <= maxx and  miny <= p0[1] <= maxy:
        return True
    else:
        return False


def isZero(number):
    return numpy.abs(number) <= EPS


def det(p1, p2, p3, p4):
    return numpy.linalg.det(numpy.array([p2 - p1, p4 - p3]))


def dot(p1, p2, p3, p4):
    return numpy.dot(p2 - p1, p4 - p3)


def isIntersected(p1, p2, p3, p4):
    d1 = det(p1, p2, p1, p4)
    d2 = det(p1, p2, p1, p3)
    d3 = det(p3, p4, p3, p1)
    d4 = det(p3, p4, p3, p2)

    if d1 * d2 <= 0 and d3 * d4 <= 0:
        return True
    else:
        return False


def lieInside(p1, p2, p3, p4):
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
            return True
        else:
            return False
    else:
        return False


def next(i, n):
    return i+1 if i+1 != n else 0


def prev(i, n):
    return i-1 if i-1 != -1 else n-1


def getSide(p0, p1, p2):
    det = numpy.linalg.det(numpy.array([p0 - p1, p2 - p1]))
    return -1 if det > 0 else 1 if det < 0 else 0


def belongToLine(p0, p1, p2):
    return True if getSide(p0, p1, p2) == 0 else False


p0 = numpy.array([200, 200])
DOTS = [numpy.array([100, 100]),
        numpy.array([150, 200]),
        numpy.array([150, 220]),
        numpy.array([120, 200]),
        numpy.array([100, 200]),
        numpy.array([250, 280]),
        numpy.array([400, 300])
        ]
'''DOTS = [numpy.array([100, 100]),
        numpy.array([200, 100]),
        numpy.array([180, 180]),
        numpy.array([100, 200])]'''

# опредление принадлежности точки многоугольнику
counter = 0
q = numpy.array([0, p0[1]])
i = 0
n = len(DOTS)
working = True

while working:
    j = next(i, n)
    if isIntersected(p0, q, DOTS[i], DOTS[j]):
        if belongToLine(DOTS[i], p0, q):
            while belongToLine(DOTS[j], p0, q): j = next(j, n);
            k = prev(i, n)
            while belongToLine(DOTS[k], p0, q): k = prev(k, n)
            if isIntersected(p0, q, DOTS[j], DOTS[k]):
                counter = counter + 1

            if j < i: working = False
            else: i = j
        else:
            if not belongToLine(DOTS[j], p0, q):
                counter = counter + 1
            i = i + 1
    else:
        i = i+1
    if i == n:
        working = False

#print(counter)
if counter % 2 == 0:
    print("outside")
else:
    print("inside")








def renderText(sc, message, p):
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))

while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)

    # Draw
    prev = DOTS[len(DOTS)-1]
    for point in DOTS:
        pygame.draw.circle(sc, BLACK, point.tolist(), RADIUS)
        pygame.draw.line(sc, BLACK, prev.tolist(), point.tolist(), RADIUS)
        prev = point

    pygame.draw.circle(sc, (0, 0, 255), p0, RADIUS)

    pygame.display.update()

    clock.tick(FPS)

