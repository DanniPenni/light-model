import pygame
from sys import exit


class Cartesian:
    def __init__(self, x, y, Z=1.0):
        self.x = x
        self.y = y
        self.z = Z
        self.simplify()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def simplify(self):
        raise NotImplementedError("Simplify Method Not Implemented.")

    def print_self(self):
        raise NotImplementedError("Print Self Method Not Implemented")


class CartPoint(Cartesian):
    def __init__(self, x, y, z=1.0):
        super().__init__(x, y, z)

    def simplify(self):
        if self.z != 1 and self.z != 0:
            self.x = round(self.x / self.z, 3)
            self.y = round(self.y / self.z, 3)
            self.z = 1.0

    def in_segment(self, line):
        bigger_x = max(line.get_points()[0].get_x(), line.get_points()[1].get_x())
        smaller_x = min(line.get_points()[0].get_x(), line.get_points()[1].get_x())
        bigger_y = max(line.get_points()[0].get_y(), line.get_points()[1].get_y())
        smaller_y = min(line.get_points()[0].get_y(), line.get_points()[1].get_y())
        return smaller_x <= self.x <= bigger_x and smaller_y <= self.y <= bigger_y

    def is_intersect_point(self, line1, line2):
        l1i = self.in_segment(line1)
        l2i = self.in_segment(line2)
        if l1i and l2i:
            if self.z == 0:
                print("Error: Parallel/Same")
                return 0
            return 1
        return 0

    def print_self(self):
        print("The coordinates of the point are:")
        print(f'({self.x}, {self.y}, {self.z})')

    def get_normal_tuple(self):
        return self.x, self.y


class Point:
    def create_cartisian(self):
        return CartPoint(self.x, self.y)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Cart = self.create_cartisian()

    def set_xy(self, x=None, y=None):
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.Cart = self.create_cartisian()

    def get_tup(self):
        return self.x, self.y

    def get_cart(self):
        return self.Cart


class CartLine(Cartesian):
    def simplify(self):
        denom1 = gcd(self.x, self.y)
        denom2 = gcd(self.y, self.z)
        denomf = gcd(denom1, denom2)

        self.x /= denomf
        self.y /= denomf
        self.z /= denomf

    def __init__(self, x, y, Z=1, Point1=None, Point2=None):
        super().__init__(x, y, Z)
        self.points = (Point1, Point2)

    def get_points(self):
        return self.points

    def print_self(self):
        sign = '+' if self.z >= 0 else '-'
        print("The equation for your line is:")
        print(f'{self.y}y = {-self.x}x {sign} {abs(self.z)}')


class Line:
    def create_cartisian(self):
        return cross_product(self.points[0].get_cart(), self.points[1].get_cart(), getLine=True)

    def __init__(self, p1, p2):
        if not isinstance(p1, Point):
            p1 = Point(p1[0], p1[1])
            p2 = Point(p2[0], p2[1])
        self.points = [p1, p2]
        self.color = "White"
        self.Cart = self.create_cartisian()

    def draw(self):
        pygame.draw.line(screen, self.color, self.points[0].get_tup(), self.points[1].get_tup())

    def change_color(self, color):
        self.color = color

    def get_cart(self):
        return self.Cart


class Ray(Line):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        self.xchange = 0
        self.ychange = 0

    def ray_update(self):
        self.points[1].set_xy(
            self.points[1].get_tup()[0] + self.xchange,
            self.points[1].get_tup()[1] + self.ychange,
        )
        self.Cart = self.create_cartisian()

    def point_movement(self, ychange=0, xchange=0):
        self.xchange = xchange
        self.ychange = ychange

    def change_points(self, changeEnd, ynew=None, xnew=None):
        self.points[changeEnd].set_xy(xnew, ynew)

    def draw(self):
        drawPoints = [point.get_tup() for point in self.points]
        pygame.draw.lines(screen, self.color, False, drawPoints)


class Block:
    def make_lines(self):
        lines = []
        for i in range(len(self.points)):
            if i == len(self.points) - 1:
                lines.append(Line(self.points[i], self.points[0]))
            else:
                lines.append(Line(self.points[i], self.points[i + 1]))
        return lines

    def __init__(self, points):
        if len(points) == 2:
            p_tl = points[0]
            p_br = points[1]
            self.points = [Point(p_tl[0], p_tl[1]), Point(p_br[0], p_tl[1]),
                           Point(p_br[0], p_br[1]), Point(p_tl[0], p_br[1])]
        elif len(points) > 2:
            self.points = [Point(p[0], p[1]) for p in points]
        self.lines = self.make_lines()

    def draw(self):
        for block_line in self.lines:
            block_line.draw()

    def check_intersections(self, ray):
        numOfInter = 0
        for block_line in self.lines:
            if line_intersect(screen, ray.get_cart(), block_line.get_cart()):
                block_line.change_color("Blue")
                numOfInter += 1
            else:
                block_line.change_color("White")
        return numOfInter


def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


def cross_product(cart1, cart2, getLine):
    res1 = cart1.y * cart2.z - cart1.z * cart2.y
    res2 = cart1.z * cart2.x - cart1.x * cart2.z
    res3 = cart1.x * cart2.y - cart1.y * cart2.x
    if getLine:
        return CartLine(res1, res2, res3, cart1, cart2)
    else:
        return CartPoint(res1, res2, res3)


def draw_inter_point(surface, center):
    pygame.draw.circle(surface, "Yellow", center, 8, 1)


def line_intersect(surface, line1, line2):
    intersectPoint = cross_product(line1, line2, getLine=False)
    if intersectPoint.is_intersect_point(line1, line2):
        print("INTERSECT OCCURRED.")
        draw_inter_point(surface, intersectPoint.get_normal_tuple())
        intersectPoint.print_self()
        return 1
    return 0


pygame.init()

screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
running = True

lightRay = Ray((0, 400), (1200, 400))
block1 = Block([(600, 100), (900, 700)])
block2 = Block([
    (300, 200), (400, 180),
    (450, 670), (300, 540),
    (200, 330)
])
blocks = [block1, block2]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                lightRay.point_movement(-1)
            elif event.key == pygame.K_DOWN:
                print("TEST")
                lightRay.point_movement(1)
        elif event.type == pygame.KEYUP:
            lightRay.point_movement(0)
    screen.fill("Black")
    lightRay.ray_update()

    for block in blocks:
        if block.check_intersections(lightRay):
            lightRay.change_color("Red")
        else:
            lightRay.change_color("White")

        block.draw()
    lightRay.draw()
    pygame.display.flip()
    clock.tick(60)


# Idea for Line-Intersection Algorithm: https://www.quora.com/How-do-I-get-the-point-of-intersection-of-two-lines-using-a-cross-product-if-I-know-two-points-of-each-line (Dean Rubine, 2019)