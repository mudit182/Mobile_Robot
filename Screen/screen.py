import pygame
from colors import *
from screenObjects import ImageObj, Polygon, Polygon2Colors, Circle, Background


class Window():
    def __init__(self, width, height, title):
        #  initialize pygame functions
        pygame.init()
        #  set thisTime (used for calculating framerate)
        self.time = pygame.time
        self.thisTime = self.time.get_ticks()
        self.frameRate = 0
        #  Set window size
        self.originalSize = (width, height)
        #  Create window !
        self.screen = pygame.display.set_mode(self.originalSize)
        #  Pack title
        self.title = title
        pygame.display.set_caption(self.title)
        #  load background, environment and car
        self._setUpBackground()

    def loadCar(self, car):
        carImgPath = 'Resources/Images/robotCar.png'
        self.car = ImageObj(carImgPath, car.size, car.location, car.orientation)

    def loadCarSensors(self, sensors):
        self.carSensors = []
        for sensor in sensors:
            self.carSensors.append(Polygon2Colors(sensor.vertices, LIGHTPINK))

    def loadObstacles(self, obstacles):
        self.obstacles = []
        for obstacle in obstacles:
            self.obstacles.append(Polygon(obstacle.vertices))

    def loadGoal(self, goal):
        self.goal = Circle(goal, 10)

    def draw(self, car, sensors):
        self._refreshBackground()
        #  draw walls
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        #  draw goal
        self.goal.draw(self.screen)
        #  draw car sensors
        for i in range(len(self.carSensors)):
            self.carSensors[i].updateDraw(self.screen, sensors[i].vertices, sensors[i].active)
        #  display car (to new position and orientation)
        self.car.updateDraw(self.screen, car.location, car.orientation)
        #  draw actual pixels on screen
        pygame.display.update()
        # And finally calculate framerate
        self._calculateFrameRate()

    def _setUpBackground(self):
        #  load background
        bgImgPath = 'Resources/Images/background.jpg'
        self.background = Background(bgImgPath, [0, 0])

    def _refreshBackground(self):
        #  display background
        self.screen.fill(WHITE)
        # self.screen.blit(self.background.image, self.background.rect)

    def _calculateFrameRate(self):
        self.lastTime = self.thisTime
        self.thisTime = self.time.get_ticks()
        self.frameRate = (self.thisTime - self.lastTime) / 1000
        return self.frameRate
