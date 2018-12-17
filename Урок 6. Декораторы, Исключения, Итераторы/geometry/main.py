import turtle
import math
import itertools



import time


class Vector(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, k):

        return Vector(self.x * k, self.y * k)

    def __add__(self, another):

        return Vector(self.x + another.x, self.y + another.y)

    def __sub__(self, another):
        
        return Vector(self.x - another.x, self.y - another.y)

    def __div__(self, k):
        return Vector(self.x / k, self.y / k)

    def __repr__(self):
        return 'V({}, {})'.format(self.x, self.y)

class Circle(object):

    def __init__(self, ttl, x, y, radius, color):

        self.ttl = ttl
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        self.ttl.color(self.color)
        self.ttl.penup()
        self.ttl.setpos(self.x, self.y - self.radius)
        self.ttl.pendown()
        self.ttl.circle(self.radius)

    def scale(self, k):
        self.radius *= k

    def move(self, x, y):
        self.x += x
        self.y += y

    def rotate(self, angle):
        pass

class Poly(object):

    def __init__(self, ttl, vertex_list, color):

        self.vertex_list = vertex_list
        self.color = color
        self.ttl = ttl

    def draw(self):

        self.ttl.color(self.color)
        last = self.vertex_list[-1]
        self.ttl.penup()
        self.ttl.setpos(last.x, last.y)
        self.ttl.pendown()
        for v in self.vertex_list:
            self.ttl.goto(v.x, v.y)
        self.ttl.penup()

    def scale(self, point, k):
        for i, v in enumerate(self.vertex_list):
            self.vertex_list[i] = (v - point) * k + point

    def move(self, x, y):
        for i, v in enumerate(self.vertex_list):
            self.vertex_list[i] = v + Vector(x, y)

    def rotate(self, point, angle):
        for i, v in enumerate(self.vertex_list):
            b = v - point
            self.vertex_list[i] = Vector(b.x * math.cos(angle) - b.y * math.sin(angle),
                                        b.x * math.sin(angle) + b.y * math.cos(angle)) + point

class RightPoly(Poly):

    def scale(self, k):
        super(RightPoly, self).scale(self._get_center(), k)

    def rotate(self, angle):
        super(RightPoly, self).rotate(self._get_center(), angle)


class Rect(RightPoly):

    def __init__(self, ttl, x, y, width, heigh, color):
        vertex_list = [Vector(x - width/2, y - heigh/2),
                        Vector(x + width/2, y - heigh/2),
                        Vector(x + width/2, y + heigh/2),
                        Vector(x - width/2, y + heigh/2)]
        return super(Rect, self).__init__(ttl, vertex_list, color)

    def _get_center(self):
        return (self.vertex_list[0] + self.vertex_list[2]) / 2

class Triagle(RightPoly):

    def __init__(self, ttl, x, y, width, color):
        heigh = math.sqrt(3) * width / 2
        vertex_list = [Vector(x - width/2, y - heigh / 2),
                        Vector(x + width/2, y - heigh/2),
                        Vector(x, y + heigh/2)]
        return super(Triagle, self).__init__(ttl, vertex_list, color)

    def _get_center(self):
        return ((self.vertex_list[0] + self.vertex_list[1])/ 2 + self.vertex_list[2]) / 2



screen = turtle.Screen()
turtle.tracer(0, 0)
turtle.hideturtle()

ttl = turtle.Turtle()
ttl.hideturtle()

p1 = Rect(ttl, 0, 0, 100, 100, 'red')

c1 = Circle(ttl, 0, 0, 50, 'violet')
direction = itertools.cycle([1] * 10 + [-1] * 10)
k = 1.1

scene = [p1, c1]


group1 = [Triagle(ttl, 200, -200, 35, 'orange'), Circle(ttl, 150, -200, 20, 'green'), Triagle(ttl, 100, -200, 35, 'orange')]
group2 = [Triagle(ttl, -200, 200, 35, 'orange'), Circle(ttl, -150, 200, 20, 'green'), Triagle(ttl, -100, 200, 35, 'orange')]

scene.extend(group1)
scene.extend(group2)



while True:

    time.sleep(0.2)
    ttl.clear()
    for x in scene:
        x.draw()

    cur_dir = direction.next()

    p1.scale(k if cur_dir == 1 else 1/k)
    p1.rotate(0.1)
    c1.scale(1 / k if cur_dir == 1 else k)

    for x in group1:
        x.move(-40 * cur_dir, 0)
        x.rotate(-0.3)

    for x in group2:
        x.move(40 * cur_dir, 0)
        x.rotate(-0.3)


    turtle.update()