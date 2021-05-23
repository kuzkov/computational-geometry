import pygame
import sys
import random
import time
from closestPairAlgorithm import *
from circle import Circle
from constants import *


pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
sc.fill(WHITE)
pygame.display.update()

circles = []
faced_circles = set()
for i in range(20):  # задание кругов
    circles.append(Circle.generate_random_circle(50, WIN_WIDTH - 50, 50, WIN_HEIGHT - 50, 5, 5))

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
    sc.fill(WHITE)
    pygame.draw.lines(sc, BLACK, True, [[HORIZONTAL_BORDER_SPACING, VERTICAL_BORDER_SPACING],
                                        [HORIZONTAL_BORDER_SPACING, WIN_HEIGHT - VERTICAL_BORDER_SPACING],
                                        [WIN_WIDTH - HORIZONTAL_BORDER_SPACING, WIN_HEIGHT - VERTICAL_BORDER_SPACING],
                                        [WIN_WIDTH - HORIZONTAL_BORDER_SPACING, VERTICAL_BORDER_SPACING]])
    for circle in circles:
        pygame.draw.circle(sc, BLACK, circle.to_list(), RADIUS)
        circle.border_strike()  # проверка на столкновение с границей и реакция на него
        circle.move()
    if len(find_closest_points(circles, faced_circles)[1]) != 0:  # нахождение столкнувшихся точек и мин расстояния
        for circle in faced_circles:
            circle.reverse_velocity_vector()
            circle.move()
    faced_circles.clear()
    pygame.display.update()
    clock.tick(FPS)
