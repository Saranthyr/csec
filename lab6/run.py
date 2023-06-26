import random

from diagram import Diagram
from point import Point


def generate_points(a, b, p):
    points = []

    for x in range(p):
        for y in range(p):
            point = Point(x, y, a, b, p)
            if point.on_curve():
                points.append((x, y))

    return points

def isprime(num):
    for n in range(2,int(num**0.5)+1):
        if num%n==0:
            return False
    return True



print('Enter the parameters for equation')
a = int(input('Parameter a\n'))
b = int(input('Parameter b\n'))

while True:
    num_pts = int(input('Number of points (prime number)\n'))
    if not isprime(num_pts):
        print("Incorrect number - not prime\n")
    else:
        break

points = generate_points(a, b, num_pts)
print("Total points:", len(points))
print("Points:", points)

diagram = Diagram(points)
diagram.plot()

choice = int(input('Select operation:\n \t 1 - Sum 2 points of curve \n \t 2 - Double points of curve\n'))

if choice == 1:
    p1_sel = random.randint(0, num_pts-1)
    p1 = Point(points[p1_sel][0], points[p1_sel][1], a, b, num_pts)
    p2_sel = random.randint(0, num_pts - 1)
    if p2_sel == p1_sel:
        p2_sel = random.randint(0, num_pts - 1)
    p2 = Point(points[p2_sel][0], points[p2_sel][1], a, b, num_pts)
    p3 = p1.sum(p2)

    print("Point 1 - purple =", p1)
    print("Point 2 - yellow =", p2)
    print("Sum of P1 and P2 =", p3, " - black")

    diagram = Diagram(points, p1, p2, p3)
    diagram.plot()
else:
    g_sel = random.randint(0, num_pts - 1)
    g = Point(points[g_sel][0], points[g_sel][1], a, b, num_pts)
    g2 = g.double_point()
    g4 = g2.double_point()

    print("Original point - purple =", g)
    print("point doubled - yellow =", g2)
    print("point quadrupled - black =", g4)

    diagram = Diagram(points, g, g2, g4)
    diagram.plot()
