
import pygame

class Road:
    def __init__(self):
        self.inner_walls = [RoadWall(188, 540, 229, 549), RoadWall(229, 549, 260, 584), RoadWall(260, 584, 266, 625), RoadWall(266, 625, 268, 644), RoadWall(268, 644, 443, 653), RoadWall(443, 653, 630, 660), RoadWall(630, 660, 848, 652), RoadWall(848, 652, 1001, 645), RoadWall(1001, 645, 1151, 638), RoadWall(1151, 638, 1251, 594), RoadWall(1251, 594, 1300, 473), RoadWall(1300, 473, 1323, 359), RoadWall(1323, 359, 1296, 234), RoadWall(1296, 234, 1266, 216), RoadWall(1266, 216, 1243, 224), RoadWall(1243, 224, 1212, 286), RoadWall(1212, 286, 1182, 402), RoadWall(1182, 402, 1131, 540), RoadWall(1131, 540, 1043, 633), RoadWall(1043, 633, 804, 643), RoadWall(804, 643, 601, 649), RoadWall(601, 649, 439, 589), RoadWall(439, 589, 375, 463), RoadWall(375, 463, 398, 333), RoadWall(398, 333, 507, 247), RoadWall(507, 247, 612, 196), RoadWall(612, 196, 643, 173), RoadWall(643, 173, 623, 155), RoadWall(623, 155, 418, 170), RoadWall(418, 170, 271, 168), RoadWall(271, 168, 189, 190), RoadWall(189, 190, 169, 292), RoadWall(169, 292, 161, 369), RoadWall(161, 369, 156, 446), RoadWall(156, 446, 158, 505), RoadWall(158, 505, 188, 540)]
        self.outer_road = [RoadWall(33, 612, 94, 624), RoadWall(94, 624, 139, 683), RoadWall(139, 683, 154, 736), RoadWall(154, 736, 261, 764), RoadWall(261, 764, 513, 761), RoadWall(513, 761, 758, 761), RoadWall(758, 761, 1125, 759), RoadWall(1125, 759, 1321, 744), RoadWall(1321, 744, 1393, 684), RoadWall(1393, 684, 1443, 569), RoadWall(1443, 569, 1463, 400), RoadWall(1463, 400, 1452, 262), RoadWall(1452, 262, 1430, 106), RoadWall(1430, 106, 1371, 45), RoadWall(1371, 45, 1215, 35), RoadWall(1215, 35, 1074, 96), RoadWall(1074, 96, 1030, 244), RoadWall(1030, 244, 992, 386), RoadWall(992, 386, 935, 510), RoadWall(935, 510, 760, 525), RoadWall(760, 525, 621, 507), RoadWall(621, 507, 563, 433), RoadWall(563, 433, 581, 370), RoadWall(581, 370, 690, 318), RoadWall(690, 318, 800, 260), RoadWall(800, 260, 852, 192), RoadWall(852, 192, 868, 115), RoadWall(868, 115, 789, 47), RoadWall(789, 47, 582, 39), RoadWall(582, 39, 411, 38), RoadWall(411, 38, 255, 43), RoadWall(255, 43, 111, 59), RoadWall(111, 59, 44, 119), RoadWall(44, 119, 22, 224), RoadWall(22, 224, 25, 320), RoadWall(25, 320, 27, 450), RoadWall(27, 450, 33, 612)]
        self.road_walls = self.inner_walls + self.outer_road
        self.gates = [RoadGate(181.0, 371.0, 8.0, 371.0), RoadGate(207.0, 208.0, 30.0, 107.0), RoadGate(435.0, 186.0, 433.0, 19.0), RoadGate(622.0, 172.0, 877.0, 176.0), RoadGate(373.0, 370.0, 587.0, 408.0), RoadGate(563.0, 645.0, 650.0, 491.0), RoadGate(809.0, 647.0, 804.0, 505.0), RoadGate(1204.0, 385.0, 971.0, 344.0), RoadGate(1274.0, 240.0, 1274.0, 24.0), RoadGate(1300.0, 382.0, 1484.0, 400.0), RoadGate(1145.0, 620.0, 1154.0, 773.0), RoadGate(696.0, 651.0, 687.0, 775.0), RoadGate(289.0, 632.0, 134.0, 749.0), RoadGate(186.0, 322.0, 7.0, 310.0), RoadGate(192.0, 264.0, 11.0, 202.0), RoadGate(244.0, 188.0, 125.0, 32.0), RoadGate(294.0, 187.0, 256.0, 27.0), RoadGate(371.0, 187.0, 352.0, 16.0), RoadGate(482.0, 184.0, 495.0, 20.0), RoadGate(549.0, 178.0, 568.0, 20.0), RoadGate(591.0, 175.0, 654.0, 19.0), RoadGate(607.0, 175.0, 781.0, 22.0), RoadGate(612.0, 177.0, 887.0, 76.0), RoadGate(587.0, 193.0, 816.0, 288.0), RoadGate(517.0, 217.0, 680.0, 364.0), RoadGate(395.0, 293.0, 634.0, 389.0), RoadGate(348.0, 473.0, 626.0, 435.0), RoadGate(403.0, 589.0, 652.0, 446.0), RoadGate(631.0, 656.0, 701.0, 490.0), RoadGate(725.0, 650.0, 738.0, 503.0), RoadGate(912.0, 644.0, 850.0, 469.0), RoadGate(1081.0, 615.0, 916.0, 461.0), RoadGate(1169.0, 507.0, 949.0, 410.0), RoadGate(1223.0, 321.0, 997.0, 224.0), RoadGate(1251.0, 271.0, 1018.0, 113.0), RoadGate(1258.0, 248.0, 1129.0, 25.0), RoadGate(1282.0, 259.0, 1411.0, 29.0), RoadGate(1280.0, 288.0, 1466.0, 146.0), RoadGate(1282.0, 329.0, 1484.0, 289.0), RoadGate(1278.0, 425.0, 1486.0, 488.0), RoadGate(1261.0, 489.0, 1461.0, 606.0), RoadGate(1234.0, 551.0, 1427.0, 710.0), RoadGate(1206.0, 586.0, 1243.0, 766.0), RoadGate(1071.0, 626.0, 1072.0, 774.0), RoadGate(936.0, 640.0, 933.0, 779.0), RoadGate(848.0, 645.0, 826.0, 784.0), RoadGate(757.0, 648.0, 753.0, 776.0), RoadGate(595.0, 653.0, 583.0, 777.0), RoadGate(483.0, 631.0, 472.0, 780.0), RoadGate(406.0, 631.0, 378.0, 785.0), RoadGate(344.0, 627.0, 259.0, 782.0), RoadGate(279.0, 561.0, 94.0, 678.0), RoadGate(220.0, 526.0, 13.0, 565.0), RoadGate(996.0, 639.0, 1001.0, 770.0), RoadGate(1232.0, 583.0, 1341.0, 758.0), RoadGate(552.0, 205.0, 727.0, 339.0), RoadGate(611.0, 185.0, 859.0, 241.0), RoadGate(440.0, 255.0, 655.0, 377.0), RoadGate(204.0, 294.0, 6.0, 257.0), RoadGate(265.0, 184.0, 204.0, 31.0), RoadGate(227.0, 199.0, 57.0, 69.0), RoadGate(326.0, 184.0, 286.0, 29.0), RoadGate(350.0, 180.0, 320.0, 24.0), RoadGate(396.0, 189.0, 394.0, 23.0)]
        self.finish_line = RoadFinishline(181.0, 500.0, 8.0, 500.0)


    def draw(self, window):
        p = [w.start for w in self.outer_road]
        pygame.draw.polygon(window, (150, 150, 150), p, 0)

            
        p = [w.start for w in self.inner_walls]
        pygame.draw.polygon(window, (51, 51, 51), p, 0)
        
        for wall in self.road_walls:
            wall.draw(window)
               
        for gate in self.gates:
            gate.draw(window)
        
        self.finish_line.draw(window)
            
    def reset(self):
        for gate in self.gates:
            gate.reset()
      

class RoadFinishline:
    def __init__(self, x1, y1, x2, y2):
        self.start = pygame.math.Vector2(x1, y1)
        self.stop = pygame.math.Vector2(x2, y2)
        self.color = (0, 0, 255)
        self.stroke = 3
        self.touching = False
        self.point = 100
        
    def __str__(self) -> str:
        return f"RoadFinishline({self.start.x}, {self.start.y}, {self.stop.x}, {self.stop.y})"
            
    def __repr__(self) -> str:
        return self.__str__()
    
    def draw(self, window):
        pygame.draw.line(window, self.color, self.start, self.stop, self.stroke)
          

class RoadGate:
    def __init__(self, x1, y1, x2, y2):
        self.start = pygame.math.Vector2(x1, y1)
        self.stop = pygame.math.Vector2(x2, y2)
        self.active = True
        self.active_color = (255, 255, 0)
        self.disabled_color = (120, 120, 0)
        self.stroke = 3
        self.touching = False
        self.point = 10
        
    def __str__(self) -> str:
        return f"RoadGate({self.start.x}, {self.start.y}, {self.stop.x}, {self.stop.y})"
    
    def __repr__(self) -> str:
        return self.__str__()
        
    def reset(self):
        self.touching = False
        self.active = True
    
    def draw(self, window):
        if self.active:
            pygame.draw.line(window, self.active_color, self.start, self.stop, self.stroke)
        else:
            pygame.draw.line(window, self.disabled_color, self.start, self.stop, self.stroke)
            
class RoadWall:
    def __init__(self, x1, y1, x2, y2):
        self.start = pygame.math.Vector2(x1, y1)
        self.stop = pygame.math.Vector2(x2, y2)
        self.main_color = (150, 150, 150)
        self.color = self.main_color
        self.main_stroke = 5
        self.stroke = self.main_stroke
        self.point = -50
    
    def __str__(self) -> str:
        return f"RoadWall({self.start.x}, {self.start.y}, {self.stop.x}, {self.stop.y})"
    
    def __repr__(self) -> str:
        return self.__str__()
        
    def draw(self, window):
        pygame.draw.line(window, self.color, self.start, self.stop, self.stroke)