import pyglet, math
from pyglet.window import key

import ctypes
user32 = ctypes.windll.user32
SCREENSIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

class Car:
    # Car placement and size
    x = 400
    y = 100
    WIDTH = 25
    HEIGHT = 35

    # Physics Controls
    VEL_X, VEL_Y = 0, 0
    ACCELERATION = 8
    DRAG = 0.95
    ANGULAR_VEL = 0
    TURN_SPEED = 1.7
    ANGULAR_DRAG = 0.8

    # Movement controls
    FORWARD = False
    LEFT = False
    RIGHT = False

    ALIVE = True

    SIGHT_DISTANCE = 300

    point = (400, 100)

    def __init__(self, angle=0):
        self.angle = angle

        self.rays = []
        for i in range(-60, 61, 30):
            self.rays.append(Ray(angle=i-90, max_length=self.SIGHT_DISTANCE))

    def get_vertices(self):
        hypot = math.hypot(self.WIDTH/2, self.HEIGHT/2)
        angle = -math.radians(self.angle-90)
        theta = math.atan(self.WIDTH/self.HEIGHT)
        x_vertex_val = hypot*math.sin(angle+theta)
        y_vertex_val = hypot*math.cos(angle+theta)
        self.vertices = ([self.x+hypot*math.sin(angle-theta), self.y+hypot*math.cos(angle-theta)],
                         [self.x+hypot*math.sin(angle+theta), self.y+hypot*math.cos(angle+theta)],
                         [self.x+hypot*math.sin(angle-theta+math.pi), self.y+hypot*math.cos(angle-theta+math.pi)],
                         [self.x+hypot*math.sin(angle+theta+math.pi), self.y+hypot*math.cos(angle+theta+math.pi)])

    def move(self):
        # This controls the physics of the car
        self.x += self.VEL_X
        self.y += self.VEL_Y
        self.VEL_X *= self.DRAG
        self.VEL_Y *= self.DRAG
        self.angle += self.ANGULAR_VEL
        self.ANGULAR_VEL *= self.ANGULAR_DRAG

        speed = math.sqrt(self.VEL_X**2 + self.VEL_Y**2)

        if self.FORWARD:
            angle_rad = math.radians(self.angle)

            self.VEL_X = math.cos(angle_rad) * self.ACCELERATION
            self.VEL_Y = math.sin(angle_rad) * self.ACCELERATION

        if speed > 0:
            if self.LEFT:
                self.ANGULAR_VEL += self.TURN_SPEED * speed / (self.ACCELERATION * self.DRAG)
            elif self.RIGHT:
                self.ANGULAR_VEL -= self.TURN_SPEED * speed / (self.ACCELERATION * self.DRAG)

        self.check_bounds()

    def check_bounds(self):
        if self.x <= 0:
            self.x = SCREENSIZE[0]
        elif self.x >= SCREENSIZE[0]:
            self.x = 0
        if self.y <= 0:
            self.y =SCREENSIZE[1]
        elif self.y >= SCREENSIZE[1]:
            self.y = 0

    def draw_car(self):
        self.get_vertices()
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                    ('v2f', (self.vertices[0][0], self.vertices[0][1],
                                             self.vertices[1][0], self.vertices[1][1],
                                             self.vertices[2][0], self.vertices[2][1],
                                             self.vertices[3][0], self.vertices[3][1])),
                                    ('c3B', (0, 200, 255,
                                             0, 200, 255,
                                             150, 0, 180,
                                             150, 0, 180)))

    def look(self, walls):
        self.SPACE_STATE = []
        for ray in self.rays:
            CLOSEST_WALL = self.SIGHT_DISTANCE
            CLOSEST_POINT = None
            for wall in walls:
                pt = ray.cast(self.x, self.y, self.angle, wall)
                if pt:
                    dist = math.dist(pt, (self.x, self.y))
                    if dist < CLOSEST_WALL:
                        CLOSEST_WALL = dist
                        CLOSEST_POINT = pt

            ray.draw(self.x, self.y, self.angle, CLOSEST_POINT)
            self.SPACE_STATE.append(CLOSEST_WALL / self.SIGHT_DISTANCE)

        return self.SPACE_STATE

    def check_collision(self, walls):
        self.get_vertices()
        for wall in walls:
            for line in range(len(self.vertices)):
                intersection = self.check_intersection(line_1=(wall.a, wall.b),
                                                       line_2=(self.vertices[line-1],
                                                               self.vertices[line]))
                if intersection:
                    self.ALIVE = False
                    return True

    def check_intersection(self, line_1, line_2):
        den = (line_1[0][0] - line_1[1][0])*(line_2[0][1] - line_2[1][1]) - (line_1[0][1] - line_1[1][1])*(line_2[0][0] - line_2[1][0])
        if den == 0:
            return
        t =  ((line_1[0][0] - line_2[0][0])*(line_2[0][1] - line_2[1][1]) - (line_1[0][1] - line_2[0][1])*(line_2[0][0] - line_2[1][0])) / den
        u = -((line_1[0][0] - line_1[1][0])*(line_1[0][1] - line_2[0][1]) - (line_1[0][1] - line_1[1][1])*(line_1[0][0] - line_2[0][0])) / den
        if t > 0 and t < 1 and u > 0 and u < 1:
            pt = [0,0]
            pt[0] = int(line_1[0][0] + t * (line_1[1][0] - line_1[0][0]))
            pt[1] = int(line_1[0][1] + t * (line_1[1][1] - line_1[0][1]))
            return True
        else:
            return

    def update_score(self):
        # self.point = (self.x, self.y)
        if math.dist(self.point, (self.x, self.y)) >= 500:
            self.point = (self.x, self.y)
            return True



class ManualCar(Car):
    def __init__(self, angle=0):
        super().__init__(angle)

    def __str__(self):
        return 'ManualCar'

    def controls(self, keys):
        if keys[key.W]:
            self.FORWARD = True
        else:
            self.FORWARD = False
        if keys[key.A]:
            self.LEFT = True
        else:
            self.LEFT = False
        if keys[key.D]:
            self.RIGHT = True
        else:
            self.RIGHT = False

        self.move()


class AutoCar(Car):
    SPACE_STATE = []

    def __init__(self, angle=0):
        super().__init__(angle)

    def __str__(self):
        return 'AutoCar'

    def controls(self, action):
        self.FORWARD = False
        self.LEFT = False
        self.RIGHT = False

        if action == 1:
            self.FORWARD = True
        elif action == 2:
            self.FORWARD = True
            self.LEFT = True
        elif action == 3:
            self.FORWARD = True
            self.RIGHT = True
        elif action == 4:
            self.LEFT = True
        elif action == 5:
            self.RIGHT = True
        elif action == 6:
            pass

        self.move()


class Ray:
    def __init__(self, angle, max_length):
        self.offset_angle = angle
        self.max_length = max_length

    def cast(self, car_x, car_y, car_angle, wall):
        # If the two lines intersect, return the point of intersection.
        angle = -math.radians(self.offset_angle+car_angle)

        x1, y1 = wall.a[0], wall.a[1]
        x2, y2 = wall.b[0], wall.b[1]
        x3, y3 = car_x, car_y
        x4, y4 = car_x+self.max_length*math.sin(angle), car_y+self.max_length*math.cos(angle)

        den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
        if den == 0:
            return
        t =  ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
        u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den
        if t > 0 and t < 1 and u > 0 and u < 1:
            pt = [0,0]
            pt[0] = int(x1 + t * (x2 - x1))
            pt[1] = int(y1 + t * (y2 - y1))
            return pt
        else:
            return

    def draw(self, car_x, car_y, car_angle, pt=None):
        angle = -math.radians(self.offset_angle+car_angle)
        if not pt:
            end = [car_x+self.max_length*math.sin(angle), car_y+self.max_length*math.cos(angle)]
            color = ('c3B', (0, 200, 255,
                             0, 200, 255))
        else:
            end = pt
            color = ('c3B', (255, 100, 55,
                             255, 100, 55))


        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                    ('v2f', (car_x, car_y,
                                             end[0], end[1])),
                                    color)
