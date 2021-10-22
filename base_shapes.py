import pyglet

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = [250,250,250] * 2
        self.line_thickness = 1

    def draw(self):
        pyglet.gl.glLineWidth(self.line_thickness)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                    ('v2f', (self.x1, self.y1,
                                             self.x2, self.y2)),
                                    ('c3B', self.color))

    def set_color(self, new_color):
        self.color = new_color * 2

    def set_line_thickness(self, new_line_thickness):
        self.line_thickness = new_line_thickness


class Rectangle:
    def __init__(self, x, y, width, height, angle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.color = [0,50,200] * 4
        self.line_thickness = 1

    def draw(self):
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                    ('v2f', (self.vertices[0][0], self.vertices[0][1],
                                             self.vertices[1][0], self.vertices[1][1],
                                             self.vertices[2][0], self.vertices[2][1],
                                             self.vertices[3][0], self.vertices[3][1])),
                                    ('c3B', self.color))

    def set_color(self, new_color):
        self.color = new_color * 4
