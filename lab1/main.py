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

p0 = numpy.array([200, 50])
p1 = numpy.array([200, 100])
p2 = numpy.array([100, 300])

FONT = pygame.font.Font(None, 20)

def getSide(p0, p1, p2):
    det = numpy.linalg.det(numpy.array([p0 - p1, p2 - p1]))
    return -1 if det > 0 else 1 if det < 0 else 0

print(getSide(p0, p1, p2))

def renderText(sc, message, p):
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))

while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)

    # Draw
    pygame.draw.circle(sc, BLACK, p0.tolist(), RADIUS)
    pygame.draw.circle(sc, BLACK, p1.tolist(), RADIUS)
    pygame.draw.circle(sc, BLACK, p2.tolist(), RADIUS)
    pygame.draw.line(sc, BLACK, p1.tolist(), p2.tolist())

    renderText(sc, "p0", p0)
    renderText(sc, "p1", p1)
    renderText(sc, "p2", p2)

    pygame.display.update()

    clock.tick(FPS)
