import pyglet

LINES = ([20, 30, 100, 200],
          [400, 600, 900, 400])

class Track:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        self.walls = []
        for line in LINES:
            self.walls.append(Wall(line[0], line[1], line[2], line[3]))
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
