import pyglet

LINES = []
OUTER_POINTS = [[264, 64],
                [120, 235],
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
                [537, 74]]
INNER_POINTS = [[805, 226],
                [537, 143],
                [370, 170],
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
                [1120, 190]]

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
        self.wall_batch = pyglet.graphics.Batch()
        self.gate_batch = pyglet.graphics.Batch()
        self.create_reward_gates()
        self.walls = []
        for line in LINES:
            self.walls.append(Wall(line[0][0], line[0][1], line[1][0], line[1][1]))
            self.add_wall(self.walls[-1])
        for gate in self.reward_gates:
            self.add_gate(gate)

    def add_wall(self, wall):
        vertex_list = self.wall_batch.add(2, pyglet.gl.GL_LINES, None,
                                     ('v2f', (wall.a[0], wall.a[1],
                                              wall.b[0], wall.b[1])),
                                     ('c3B', (0, 200, 255,
                                              0, 200, 255)))

    def add_gate(self, gate):
        gate_list = self.gate_batch.add(2, pyglet.gl.GL_LINES, None,
                                     ('v2f', (gate.a[0], gate.a[1],
                                              gate.b[0], gate.b[1])),
                                     ('c3B', (0, 200, 255,
                                              0, 200, 255)))

    def create_reward_gates(self):
        self.reward_gates = []
        self.reward_gates.append(RewardGate(800,220,800,100))
        self.reward_gates.append(RewardGate(1050,200,1040,70))
        self.reward_gates.append(RewardGate(1300,170,1300,50))
        self.reward_gates.append(RewardGate(1320,190,1460,175))
        self.reward_gates.append(RewardGate(1325,400,1450,375))
        self.reward_gates.append(RewardGate(1360,550,1500,540))
        self.reward_gates.append(RewardGate(1340,690,1480,780))
        self.reward_gates.append(RewardGate(1250,715,1220,830))
        self.reward_gates.append(RewardGate(1175,700,980,660))
        self.reward_gates.append(RewardGate(1060,525,1200,500))
        self.reward_gates.append(RewardGate(1010,400,1160,270))
        self.reward_gates.append(RewardGate(820,400,820,280))
        self.reward_gates.append(RewardGate(630,410,550,315))
        self.reward_gates.append(RewardGate(560,470,390,490))
        self.reward_gates.append(RewardGate(480,640,650,720))
        self.reward_gates.append(RewardGate(375,690,400,800))
        self.reward_gates.append(RewardGate(180,630,70,700))
        self.reward_gates.append(RewardGate(170,515,50,500))
        self.reward_gates.append(RewardGate(215,350,70,300))
        self.reward_gates.append(RewardGate(300,230,187,110))
        self.reward_gates.append(RewardGate(500,190,430,40))
        self.reward_gates.append(RewardGate(650,200,650,65))

    def draw_track(self):
        self.wall_batch.draw()

    def draw_gates(self):
        self.gate_batch.draw()

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.a = [x1, y1]
        self.b = [x2, y2]

class RewardGate:
    def __init__(self, x1, y1, x2, y2):
        self.a = [x1, y1]
        self.b = [x2, y2]
        self.center = [(x1-x2)/2 + x2, (y1-y2)/2 + y2]
