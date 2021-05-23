from circle import Circle
from constants import RADIUS


def headlong_search(points, faced_circles):
    min_distance = Circle.find_distance_between_centers(points[0], points[1])
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = Circle.find_distance_between_centers(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
            if distance < 2 * RADIUS:  # точки столкнулись
                faced_circles.add(points[i])
                faced_circles.add(points[j])
    return min_distance, faced_circles


def strip_closest(points, current_min_distance, faced_circles):
    n = len(points)
    min_distance = current_min_distance
    points = sorted(points, key=lambda point: point.y)

    for i in range(n):
        for j in range(i + 1, n):
            distance = Circle.find_distance_between_centers(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                if distance < 2 * RADIUS:  # точки столкнулись
                    faced_circles.add(points[i])
                    faced_circles.add(points[j])
    return min_distance, faced_circles


def find_closest_points(points, faced_circles, step=0):
    n = len(points)
    if step == 0:
        points = sorted(points, key=lambda point: point.x)
        step = 1

    if n <= 3:  # полный перебор
        return headlong_search(points, faced_circles)

    if n % 2 == 0:  # выбор средней точки
        mid_elem = int(len(points) / 2) - 1
    else:
        mid_elem = int(len(points) / 2)

    left = [i for i in points[:1 + mid_elem]]  # центральная точка + все, что левее её
    right = [i for i in points[mid_elem + 1:]]  # все точки, которые правее центральной

    min_left = find_closest_points(left, faced_circles, step)[0]  # минимальное расстояние слева от разделяющей прямой
    min_right = find_closest_points(right, faced_circles, step)[0]  # минимальное расстояние справа от разделяющей прямой

    min_distance = min(min_left, min_right)
    strip = []  # список точек, находящихся от разделяющей прямой на расстоянии, меньшем чем min_distance

    for i in range(n):
        if abs(points[i].x - points[mid_elem].x) < min_distance:
            strip.append(points[i])

    return min(min_distance, strip_closest(strip, min_distance, faced_circles)[0]), faced_circles
