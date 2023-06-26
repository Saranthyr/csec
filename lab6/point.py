class Point:
    def __init__(self, x, y, a, b, p):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.p = p

    def on_curve(self):
        y_mod_p = (self.y ** 2) % self.p
        x_ax_b_mod_p = (self.x ** 3 + self.a * self.x + self.b) % self.p
        return y_mod_p == x_ax_b_mod_p

    def sum(self, other):
        if self.x == other.x and self.y == other.y:
            return self.double_point()
        numerator = other.y - self.y
        denominator = other.x - self.x
        s = numerator * self.multiplicative_inverse(denominator) % self.p
        x3 = (s ** 2 - self.x - other.x) % self.p
        y3 = (s * (self.x - x3) - self.y) % self.p
        return Point(x3, y3, self.a, self.b, self.p)

    def double_point(self):
        numerator = 3 * self.x ** 2 + self.a
        denominator = 2 * self.y
        s = numerator * self.multiplicative_inverse(denominator) % self.p
        x3 = (s ** 2 - 2 * self.x) % self.p
        y3 = (s * (self.x - x3) - self.y) % self.p
        return Point(x3, y3, self.a, self.b, self.p)

    def multiplicative_inverse(self, a):
        a = a % self.p
        for x in range(1, self.p):
            if (a * x) % self.p == 1:
                return x
        return -1

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
