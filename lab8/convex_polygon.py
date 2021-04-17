from segment import Segment
from polygon import Polygon
import math
from vector import Vector

class ConvexPolygon(Polygon):
    # TODO: Override constructor to determine if a polygon is convex and counterclockwise

    def clip_polygon(self, polygon):
        value = self.__find_intersecting_edges(polygon)

        if value is None:
            # if self.contains(polygon.points[0]):
            #     return polygon
            # elif polygon.contains(self.points[0]):
            #     return self
            return ConvexPolygon([])

        p, q = value

        P = self.edges()
        Q = polygon.edges()

        for edge in P:
            if edge.equal(p):
                p = edge
        for edge in Q:
            if edge.equal(q):
                q = edge

        result_coords = []
        first_point = None

        k = 1
        while k < 2 * (len(P) + len(Q)):
            if p.intersects(q):
                pt = p.intersection(q)

                if first_point is None:
                    first_point = pt
                elif math.isclose(first_point.x, pt.x) and math.isclose(first_point.y, pt.y):
                    break

                result_coords.append(pt)

            advancep = False
            advanceq = False

            if (p.aimAt(q) and q.aimAt(p)) or (not p.aimAt(q) and not q.aimAt(p)) or p.is_collinear_to(q):
                if q.p2.direction(p) >= 0:
                    advanceq = True
                elif p.p2.direction(q) >= 0:
                    advancep = True
            elif p.aimAt(q):
                if p.is_inside(q):
                    result_coords.append(p.p2)
                advancep = True
            elif q.aimAt(p):
                if q.is_inside(p):
                    result_coords.append(q.p2)
                advanceq = True

            prev_q = q
            if advancep:
                for i, edge in enumerate(P):
                    if p.equal(edge):
                        p = P[(i + 1 + len(P)) % len(P)]
                        break
            if advanceq:
                for i, edge in enumerate(Q):
                    if q.equal(edge):
                        q = Q[(i + 1 + len(Q)) % len(Q)]
                        break

            k += 1

        return Polygon(result_coords)

    def __find_intersecting_edges(self, polygon):
        P = self.edges()
        Q = polygon.edges()

        p = P[0]
        q = Q[0]

        for i in range(2 * (len(P) + len(Q) + 1)):
            if p.intersects(q):
                return p, q

            p, q = self.__advance(p, q, P, Q)

        return None

    def __advance(self, p, q, P, Q):
        advancep = False
        advanceq = False

        if (p.aimAt(q) and q.aimAt(p)) or (not p.aimAt(q) and not q.aimAt(p)) or p.is_collinear_to(q):
            if q.p2.direction(p) >= 0: # q.p2 is on the right of p
                print(q.p2.direction(p))
                advanceq = True
            elif p.p2.direction(q) >= 0:
                print(p.p2.direction(q))
                advancep = True
        elif p.aimAt(q):
            advancep = True
        elif q.aimAt(p):
            advanceq = True

        if advancep:
            for i, edge in enumerate(P):
                if p is edge:
                    return P[(i + 1 + len(P)) % len(P)], q
        if advanceq:
            for i, edge in enumerate(Q):
                if q is edge:
                    return p, Q[(i + 1 + len(Q)) % len(Q)]

    def clip_segment(self, segment):
        e1 = segment.p1
        e2 = segment.p2
        D = segment.as_vector()

        min_p = 0
        max_p = 1

        size = len(self.points)

        for i in range(size):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % size]

            n = Segment(p1, p2).as_vector().get_right_normal()
            W = Segment(p1, e1).as_vector()

            if math.isclose(Vector.dot(D, n), 0):
                continue

            t = - Vector.dot(W, n) / Vector.dot(D, n)

            if not 0 <= t <= 1:
                continue



            if Vector.dot(n, D) > 0:  # Отрезок выходит из полигона
                if t < max_p: max_p = t
            else:  # Отрезок входит в полигон
                if t > min_p: min_p = t

        p1 = Vector.add(e1, Vector.mult(Vector.subtract(e2, e1), min_p))
        p2 = Vector.add(e1, Vector.mult(Vector.subtract(e2, e1), max_p))

        return Segment((p1.x, p1.y), (p2.x, p2.y))

    # Only counterclockwise
    def contains(self, point):
        n = len(self.points)
        if point.direction(Segment(self.points[0], self.points[1])) < 0 or point.direction(
                Segment(self.points[0], self.points[n - 1])) > 0:
            return False

        p, r = 1, n - 1
        while r - p > 1:
            q = (p + r) // 2
            if point.direction(Segment(self.points[0], self.points[q])) < 0:
                r = q
            else:
                p = q

        return not Segment(self.points[0], point).intersects(Segment(self.points[p], self.points[r]))