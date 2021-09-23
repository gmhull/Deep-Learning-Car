import pyglet

LINES = []
OUTER_POINTS = [[264, 44],
          [80, 200],
          [32, 650],
          [121, 770],
          [296, 811],
          [622, 784],
          [680, 655],
          [607, 545],
          [565, 472],
          [625, 408],
          [1008, 398],
          [1076, 571],
          [982, 664],
          [994, 821],
          [1338, 843],
          [1480, 781],
          [1514, 607],
          [1434, 298],
          [1470, 174],
          [1373, 45],
          [1041, 64],
          [812, 102],
          [537, 34]]
INNER_POINTS = [[805, 226],
                [537, 183],
                [369, 194],
                [246, 274],
                [172, 471],
                [180, 630],
                [281, 691],
                [456, 680],
                [503, 612],
                [391, 492],
                [436, 353],
                [658, 283],
                [1165, 272],
                [1184, 439],
                [1231, 560],
                [1174, 707],
                [1308, 719],
                [1378, 637],
                [1326, 401],
                [1299, 258],
                [1323, 168],
                [1120, 190],]

for point in range(len(OUTER_POINTS)):
    LINES.append([])
    LINES[-1].append(OUTER_POINTS[point-1])
    LINES[-1].append(OUTER_POINTS[point])
for point in range(len(INNER_POINTS)):
    LINES.append([])
    LINES[-1].append(INNER_POINTS[point-1])
    LINES[-1].append(INNER_POINTS[point])

class Track:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        self.walls = []
        for line in LINES:
            self.walls.append(Wall(line[0][0], line[0][1], line[1][0], line[1][1]))
            self.add_wall(self.walls[-1])

    def add_wall(self, wall):
        vertex_list = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                     ('v2f', (wall.a[0], wall.a[1],
                                              wall.b[0], wall.b[1])),
                                     ('c3B', (0, 200, 255,
                                              0, 200, 255)))

    def draw_track(self):
        self.batch.draw()

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.a = [x1, y1]
        self.b = [x2, y2]
