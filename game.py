import pyglet
from base_shapes import Line, Rectangle
import car


class Game:
    OBSERVATION_SPACE_VALUES = 5
    ACTION_SPACE_SIZE = 6

    def __init__(self, manual=True):
        self.MANUAL = manual

        # Initiate walls and gates
        self.walls = []
        self.reward_gates = []
        self.create_walls()
        self.create_reward_gates()

        self.create_car()

    def create_walls(self):
        # Outer Walls
        self.walls.append(Wall(120, 235, 264, 64))
        self.walls.append(Wall(32, 650, 120, 235))
        self.walls.append(Wall(121, 770, 32, 650))
        self.walls.append(Wall(296, 811, 121, 770))
        self.walls.append(Wall(622, 784, 296, 811))
        self.walls.append(Wall(680, 655, 622, 784))
        self.walls.append(Wall(607, 545, 680, 655))
        self.walls.append(Wall(565, 472, 607, 545))
        self.walls.append(Wall(625, 408, 565, 472))
        self.walls.append(Wall(1008, 398, 625, 408))
        self.walls.append(Wall(1076, 571, 1008, 398))
        self.walls.append(Wall(982, 664, 1076, 571))
        self.walls.append(Wall(994, 821, 982, 664))
        self.walls.append(Wall(1338, 843, 994, 821))
        self.walls.append(Wall(1480, 781, 1338, 843))
        self.walls.append(Wall(1514, 607, 1480, 781))
        self.walls.append(Wall(1434, 298, 1514, 607))
        self.walls.append(Wall(1470, 174, 1434, 298))
        self.walls.append(Wall(1373, 45, 1470, 174))
        self.walls.append(Wall(1041, 64, 1373, 45))
        self.walls.append(Wall(812, 102, 1041, 64))
        self.walls.append(Wall(537, 74, 812, 102))
        self.walls.append(Wall(264, 64, 537, 74))
        # Inner Walls
        self.walls.append(Wall(805, 226, 537, 143))
        self.walls.append(Wall(537, 143, 370, 170))
        self.walls.append(Wall(370, 170, 246, 274))
        self.walls.append(Wall(246, 274, 172, 471))
        self.walls.append(Wall(172, 471, 180, 630))
        self.walls.append(Wall(180, 630, 281, 691))
        self.walls.append(Wall(281, 691, 456, 680))
        self.walls.append(Wall(456, 680, 503, 612))
        self.walls.append(Wall(503, 612, 391, 492))
        self.walls.append(Wall(391, 492, 436, 353))
        self.walls.append(Wall(436, 353, 658, 283))
        self.walls.append(Wall(658, 283, 1165, 272))
        self.walls.append(Wall(1165, 272, 1184, 439))
        self.walls.append(Wall(1184, 439, 1231, 560))
        self.walls.append(Wall(1231, 560, 1174, 707))
        self.walls.append(Wall(1174, 707, 1308, 719))
        self.walls.append(Wall(1308, 719, 1378, 637))
        self.walls.append(Wall(1378, 637, 1326, 401))
        self.walls.append(Wall(1326, 401, 1299, 258))
        self.walls.append(Wall(1299, 258, 1323, 168))
        self.walls.append(Wall(1323, 168, 1120, 190))
        self.walls.append(Wall(1120, 190, 805, 226))

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

    def create_car(self):
        if self.MANUAL:
            self.car = car.ManualCar(self.reward_gates, self.walls)
        else:
            self.car = car.AutoCar(self.reward_gates, self.walls)

    def draw_track(self):
        self.wall_batch.draw()

    def reset(self):
        self.car.reset()

    def make_action(self):
        pass

    def get_score(self):
        return self.car.score

    def get_episode(self):
        pass


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.line = Line(self.x1, self.y1, self.x2, self.y2)
        self.line.set_line_thickness(2)

    def draw(self):
        self.line.draw()


class RewardGate:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.center = [(x1-x2)/2 + x2, (y1-y2)/2 + y2]
        self.active = True

        self.line = Line(self.x1, self.y1, self.x2, self.y2)
        self.line.set_color((200,150,50))

    def draw(self):
        self.line.draw()
