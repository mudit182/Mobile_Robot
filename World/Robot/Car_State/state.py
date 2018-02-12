from math import cos, sin
import numpy as np
from myMathFunctions import vectorNorm


class CarState:
    def __init__(self, type, size, location, orientation, speed, angularSpeed, goal):
        self.type = type

        self.size = np.array(size)
        self.location = np.array(location)
        self.orientation = np.array(orientation)

        self.speed = speed
        self.angularSpeed = angularSpeed

        self.goal = np.array(goal)
        self._initProgress()

    def update(self, acceleration, angularSpeed, timeElapsed):
        self.angularSpeed = angularSpeed
        self.speed += acceleration * timeElapsed

        ds = self.speed * timeElapsed
        dx, dy = ds * np.array([cos(self.orientation), sin(self.orientation)])
        da = self.angularSpeed * timeElapsed

        self.location = self.location + np.array([dx, dy])
        self.orientation += da

        self.updateProgress()

    def atGoal(self):
        if self.getDistanceToGoal() > 10:
            return False
        else:
            return True

    def updateProgress(self):

        if self.maxProgress > self.getDistanceToGoal():
            self.maxProgress = self.getDistanceToGoal()
            self.progressMade = True
        else:
            self.progressMade = False

        self.movingForward = True if self.prevDistToGoal < self.getDistanceToGoal() else False
        self.prevDistToGoal = self.getDistanceToGoal()

    def getDistanceToGoal(self):
        return vectorNorm(self.goal - self.location)

    def stopMoving(self):
        self.speed = 0
        self.angularSpeed = 0

    def _initProgress(self):
        self.maxProgress = self.getDistanceToGoal()
        self.progressMade = True
        self.prevDistToGoal = self.getDistanceToGoal()
