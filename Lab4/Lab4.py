import pygame
import sys

pygame.init()
FPS = 2
WIN_WIDTH = 600
WIN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUNNING = True

RADIUS = 3
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FONT = pygame.font.Font(None, 20)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = ""

    def to_list(self) -> list[int]:
        return [self.x, WIN_HEIGHT - self.y]

    def show(self):
        print("(", self.x, " ", self.y, ")", " ", self.name, sep="")


def get_side(p0: Point, p1: Point, p2: Point) -> int:
    det = (p2.x - p1.x) * (p0.y - p1.y) - (p2.y - p1.y) * (p0.x - p1.x)
    if det > 0:
        return -1  # левее
    elif det < 0:
        return 1  # правее
    else:
        return 0  # лежит на прямой


def find_start_point_index(points_list: list[Point]) -> int:  # поиск начальной точки
    min_y = points_list[0].y
    min_x_with_min_y = points_list[0].x
    index = 0
    for point in points_list:
        if point.y < min_y:
            min_y = point.y
            min_x_with_min_y = point.x
    i = 0
    for point in points_list:
        if point.y == min_y:
            if min_x_with_min_y >= point.x:
                min_x_with_min_y = point.x
                index = i
        i += 1
    return index


def find_cos(p0: Point, p1: Point) -> float:
    a = Point(p1.x - p0.x, p1.y - p0.y)
    b = Point(1, 0)
    angle = round((a.x * b.x + a.y * b.y) / (a.x * a.x + a.y * a.y) ** (1 / 2), 12)
    return angle


# сортировка точек по полярному углу относительно начальной
def angle_sort(points_list: list[Point], start_point: Point) -> list[Point]:
    angle_array = []
    for i in range(len(points_list)):
        angle_array.append(find_cos(start_point, points_list[i]))
    for i in range(len(points_list) - 1):
        for j in range(len(points_list) - 1 - i):
            if angle_array[j] < angle_array[j + 1]:
                angle_array[j], angle_array[j + 1] = angle_array[j + 1], angle_array[j]
                points_list[j], points_list[j + 1] = points_list[j + 1], points_list[j]
            if angle_array[j] == angle_array[j + 1]:  # если углы равны
                if points_list[j].x == start_point.x and points_list[j].y < points_list[j + 1].y:  # x точек = x начальной точки
                    angle_array[j], angle_array[j + 1] = angle_array[j + 1], angle_array[j]
                    points_list[j], points_list[j + 1] = points_list[j + 1], points_list[j]
                    continue
                if points_list[j].y == points_list[j + 1].y and points_list[j].x > points_list[j + 1].x:  # y точек = y начальной точки
                    angle_array[j], angle_array[j + 1] = angle_array[j + 1], angle_array[j]
                    points_list[j], points_list[j + 1] = points_list[j + 1], points_list[j]
                    continue
                if points_list[j].y > points_list[j + 1].y:  # точки не имеют общих координат с начальной точкой, но лежат на одной прямой
                    angle_array[j], angle_array[j + 1] = angle_array[j + 1], angle_array[j]
                    points_list[j], points_list[j + 1] = points_list[j + 1], points_list[j]
    # --------------------------------------------------  # проверка возможности построения выпуклой оболочки
    if len(angle_array) < 2:
        print("Impossible to build convex hull (Less then 3 points)")
        exit()
    if angle_array[len(angle_array) - 1] == angle_array[0]:
        print("Impossible to build convex hull (All points lie on one straight line)")
        exit()
    # --------------------------------------------------
    for i in range(len(points_list)):
        points_list[i].name = "p" + str(i + 1)
    return points_list


#  Draw functions
def render_text(sc, message, p) -> None:
    text = FONT.render(message, False, (0, 0, 0))
    sc.blit(text, (p[0] + 5, p[1] + 5))


def draw_points(array: list[Point]):
    for point in array:
        pygame.draw.circle(sc, BLACK, point.to_list(), RADIUS)
        render_text(sc, point.name, point.to_list())
    pygame.display.update()


def draw_lines(array: list[Point]):
    for i in range(len(array) - 1):
        pygame.draw.line(sc, BLACK, array[i].to_list(), array[i + 1].to_list())
    clock.tick(FPS)
    pygame.display.update()


while RUNNING:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(WHITE)

    points_list = [Point(120, 50), Point(250, 400), Point(320, 180), Point(240, 380), Point(540, 550), Point(400, 90),
                   Point(200, 40), Point(500, 40), Point(240, 90), Point(280, 60), Point(510, 280), Point(80, 450),
                   Point(40, 40), Point(200, 550), Point(170, 478), Point(400, 345), Point(240, 540), Point(40, 240),
                   Point(120, 120), Point(270, 270), Point(100, 560), Point(140, 70), Point(400, 180), Point(40, 380)]
    # points_list = [Point(50,50), Point(70,70),Point(200,200), Point(200,20)]
    start_point = points_list[find_start_point_index(points_list)]
    start_point.name = "p0"
    points_list.remove(start_point)  # удаление начальной точки из массива точек
    angle_sort(points_list, start_point)
    points_list.append(start_point)  # добавление начальной точки в конец массива точек

    # DRAW
    draw_points(points_list)
    answer = []
    answer.append(start_point)
    answer.append(points_list[0])
    draw_lines(answer)
    i = 1
    j = 1
    while i < len(points_list):  # алгоритм Грэхема
        # print(points_list[i].name, "added")
        answer.append(points_list[i])
        # print("current step:", points_list[i].name, answer[j - 1].name, answer[j].name)
        if get_side(points_list[i], answer[j - 1], answer[j]) <= 0:
            pygame.draw.line(sc, BLACK, answer[j].to_list(), points_list[i].to_list())
            clock.tick(FPS)
            pygame.display.update()
            j += 1
        else:
            j -= 1
            i -= 1
            # print(answer.pop().name, "deleted")
            # print(answer.pop().name, "deleted")
            answer.pop()
            answer.pop()
            sc.fill(WHITE)
            draw_lines(answer)
            draw_points(points_list)
            clock.tick(FPS)
            pygame.display.update()
        i += 1

    print("convex hull: ", end="")
    for i in range(len(answer) - 1):
        print(answer[i].name, end=" ")
    print()
    clock.tick(FPS)
    pygame.display.update()