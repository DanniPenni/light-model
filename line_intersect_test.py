def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


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
        raise NotImplementedError("Oopshie SIMPLFY")

    def print_self(self):
        raise NotImplementedError("Oopshie PRINTSELF")


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

    def print_point_validity(self, line1, line2):
        if self.z == 0:
            if self.x == 0 and self.y == 0:
                print("The two lines that you have provided are the same.")
            else:
                print("The two lines that you have provided are parallel.")
        else:
            self.print_self()
            l1i = self.in_segment(line1)
            l2i = self.in_segment(line2)

            if l1i and l2i:
                print("This point is on both segments! It is a valid point!")
            else:
                print(f'This point is {"not " if not l1i else ""}on Segment 1 and is {"not" if not l2i else ""} on '
                      f'Segment 2.')

    def print_self(self):
        print("The coordinates of the point are:")
        print(f'({self.x}, {self.y}, {self.z})')


def cross_product(cart1, cart2, getLine):
    res1 = cart1.y * cart2.z - cart1.z * cart2.y
    res2 = cart1.z * cart2.x - cart1.x * cart2.z
    res3 = cart1.x * cart2.y - cart1.y * cart2.x
    if getLine:
        return CartLine(res1, res2, res3, cart1, cart2)
    else:
        return CartPoint(res1, res2, res3)


x1, y1 = tuple(map(float, input("Please enter Point 1 of Line 1: ").strip().split()))
Point11 = CartPoint(x1, y1)
Point11.print_self()
x2, y2 = tuple(map(float, input("Please enter Point 2 of Line 1: ").strip().split()))
Point12 = CartPoint(x2, y2)
Point12.print_self()

x1, y1 = tuple(map(float, input("Please enter Point 1 of Line 2: ").strip().split()))
Point21 = CartPoint(x1, y1)
Point21.print_self()
x2, y2 = tuple(map(float, input("Please enter Point 2 of Line 2: ").strip().split()))
Point22 = CartPoint(x2, y2)
Point22.print_self()

Line1 = cross_product(Point11, Point12, getLine=True)
Line1.print_self()
Line2 = cross_product(Point21, Point22, getLine=True)
Line2.print_self()

InterPoint = cross_product(Line1, Line2, getLine=False)
InterPoint.print_point_validity(Line1, Line2)
