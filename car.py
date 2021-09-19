import pyglet, math
from pyglet.window import key

class Car:
    # Car placement and size
    x = 100
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

    def __init__(self, angle):
        self.angle = angle

        self.rays = []
        for i in range(6):
            self.rays.append(Ray(angle=i/(2*math.pi)))

    def get_vertices(self):
        hypot = math.hypot(self.WIDTH/2, self.HEIGHT/2)
        angle = -math.radians(self.angle-90)
        theta = math.atan(self.WIDTH/self.HEIGHT)
        x_vertex_val = hypot*math.sin(angle+theta)
        y_vertex_val = hypot*math.cos(angle+theta)
        self.vertices = ([int(self.x+hypot*math.sin(angle-theta)), int(self.y+hypot*math.cos(angle-theta))],
                         [int(self.x+hypot*math.sin(angle+theta)), int(self.y+hypot*math.cos(angle+theta))],
                         [int(self.x+hypot*math.sin(angle-theta+math.pi)), int(self.y+hypot*math.cos(angle-theta+math.pi))],
                         [int(self.x+hypot*math.sin(angle+theta+math.pi)), int(self.y+hypot*math.cos(angle+theta+math.pi))])

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

        # self.check_bounds()

    def check_bounds(self):
        if self.x == 0:
            self.x = self.get_size()[0]
        elif self.x == self.get_size()[0]:
            self.x = 0
        if self.y == 0:
            self.y =self.get_size()[1]
        elif self.y == self.get_size()[1]:
            self.y = 0

    def draw_car(self):
        self.get_vertices()
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                    ('v2i', (self.vertices[0][0], self.vertices[0][1],
                                             self.vertices[1][0], self.vertices[1][1],
                                             self.vertices[2][0], self.vertices[2][1],
                                             self.vertices[3][0], self.vertices[3][1])),
                                    ('c3B', (0, 200, 255,
                                             0, 200, 255,
                                             150, 0, 180,
                                             150, 0, 180)))

    def look(self):
        for ray in self.rays:
            ray.cast()

    def update_score(self):
        pass


class ManualCar(Car):
    def __init__(self, angle):
        super().__init__(angle)

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
    def __init__(self, angle):
        super().__init__(angle)

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
            self.RIGHT = False
        else:
            self.RIGHT = True

        self.move()

class Ray:
    length = 200
    def __init__(self, angle):
        self.offset_angle = angle

    def cast(self, car_x, car_y, car_angle):
        pass

    def draw(self, car_x, car_y, car_angle):
        pyglet.graphics.draw_indexed(2, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                    ('v2i', (x, y,
                                             self.length*math.sin(self.offset_angle+car_angle),
                                             self.length*math.cos(self.offset_angle+car_angle))),
                                    ('c3B', (0, 200, 255,
                                             0, 200, 255)))
