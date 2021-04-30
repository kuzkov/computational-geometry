import pygame
import sys
import random
import time
from point import *

pygame.init()
FPS = 5
WIN_WIDTH = 600
WIN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUNNING = True
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
sc.fill(WHITE)
pygame.display.update()
FONT = pygame.font.Font(None, 20)


def get_side(p0: Point, p1: Point, p2: Point) -> int:  # p0 относительно отрезка p1p2
    det = (p2.x - p1.x) * (p0.y - p1.y) - (p2.y - p1.y) * (p0.x - p1.x)
    if det > 0:
        return -1  # левее
    elif det < 0:
        return 1  # правее
    else:
        return 0  # лежит на прямой


def render_text(sc, message, p) -> None:
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))


def draw_hull(points):
    for i in range(len(points) - 1):
        pygame.draw.line(sc, BLACK, points[i].to_list(), points[i + 1].to_list())
        render_text(sc, str(i), points[i].to_list())
    render_text(sc, str(len(points) - 1), points[-1].to_list())
    if len(points) > 2:
        pygame.draw.line(sc, BLACK, points[0].to_list(), points[-1].to_list())


def draw_points(points, radius):
    for i in range(len(points)):
        pygame.draw.circle(sc, BLACK, points[i].to_list(), radius)


def find_visible_edges(new_point, convex_hull):  # возвращает индексы точек, которые принадлежат видимым рёбрам
    indexes = []
    for i in range(len(convex_hull) - 1):
        if get_side(new_point, convex_hull[i], convex_hull[i + 1]) > 0:
            indexes.append(i)
            indexes.append(i + 1)
    if get_side(new_point, convex_hull[-1], convex_hull[0]) > 0:  # последняя и нулевая вершины
        indexes.append(0)
        indexes.append(len(convex_hull) - 1)
    return indexes


def rebuild_hull(new_point, convex_hull):
    indexes = find_visible_edges(new_point, convex_hull)  # индексы точек, принадлежащих видимым рёбрам
    if len(indexes) == 0:
        return
    control_points = set()
    for index in indexes:  # нахождение не повторяющихся индексов в indexes: они будут индексами опорных точек
        set_size = len(control_points)
        control_points.add(index)
        if len(control_points) == set_size:
            control_points.remove(index)
    left_control_point = control_points.pop()
    right_control_point = control_points.pop()
    if get_side(convex_hull[left_control_point], convex_hull[right_control_point], new_point) == 1:
        left_control_point, right_control_point = right_control_point, left_control_point
    to_remove = []  # список точек, которые должны быть удалены из оболочки
    for ind in set(indexes):
        if ind != left_control_point and ind != right_control_point:
            to_remove.append(convex_hull[ind])  # получение ссылок на точки, которые должны быть удалены
    convex_hull.insert(right_control_point + 1, new_point)  # добавление новой точки в оболочку
    while to_remove:
        convex_hull.remove(to_remove.pop())  # удаление точек, лежащих между опорными точками, из выпуклой оболочки

points = []
convex_hull = []
while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)
    points.append(Point.generate_random_point(20, WIN_WIDTH - 20, 20, WIN_HEIGHT - 20))  # генерация рандомных точек
   # x, y = map(int, input().split())
   # points.append(Point(x, y))
    if len(convex_hull) < 3:
        convex_hull.append(points[-1])
        if len(convex_hull) == 2:
            if Point.equals(convex_hull[0], convex_hull[1]):
                convex_hull.pop()
            elif convex_hull[0].y > convex_hull[1].y or (convex_hull[0].y == convex_hull[1].y and convex_hull[0].x > convex_hull[1].x):
                convex_hull[0], convex_hull[1] = convex_hull[1], convex_hull[0]
        if len(convex_hull) == 3:
            if Point.equals(convex_hull[0], convex_hull[1]) or Point.equals(convex_hull[1], convex_hull[2]):
                convex_hull.pop()
            elif get_side(convex_hull[2], convex_hull[0], convex_hull[1]) == 1:
                convex_hull[1], convex_hull[2] = convex_hull[2], convex_hull[1]
            elif get_side(convex_hull[2], convex_hull[0], convex_hull[1]) == 0:  # ликвидация случая 3 точек на 1 прямой
                points.pop()
                convex_hull.pop()
    else:
        rebuild_hull(points[-1], convex_hull)
    draw_points(points, 2)
    draw_hull(convex_hull)
    pygame.display.update()
    clock.tick(FPS)