import numpy as np
from math import cos, sin
from myMathFunctions import intersection2Lines2D


class Sensor:
    def __init__(self, number, sensorRange, relativeOrientation, hostRobot):
        self.number = number
        self._setUp(sensorRange, relativeOrientation)
        self._resetReading()
        self.updateState(hostRobot)

    def read(self, obstacles):
        self._resetReading()
        for obstacle in obstacles:
            obstacleDistance = self._getObstacleDistance(obstacle)
            if obstacleDistance is not None:
                self.reading = min(self.reading, obstacleDistance)
        if self.reading < self.range:
            self.active = True

    def updateState(self, hostRobot):
        self.location = hostRobot.state.location + self.relativeLocation
        self.orientation = hostRobot.state.orientation + self.relativeOrientation

        self._calculateDirectionalVectors()
        self._calculateDrawPoints()

    def _setUp(self, sensorRange, relativeOrientation):
        self.range = sensorRange
        self.objectDistance = self.range
        self.relativeLocation = np.array([0.0, 0.0])
        self.relativeOrientation = relativeOrientation

    def _resetReading(self):
        self.active = False
        self.reading = self.range
        self.count = 0

    def _getObstacleDistance(self, obstacle):
        obstacleDistance = None
        for i in range(len(obstacle.vertices)):
            j = i + 1 if not (i == len(obstacle.vertices) - 1) else 0
            obstacleSide = np.array(obstacle.vertices[j]) - np.array(obstacle.vertices[i])
            intersectionData = intersection2Lines2D(self.location, self.rangeVector, obstacle.vertices[i], obstacleSide)
            if intersectionData[0] is not None:
                if intersectionData[1][1] >= 0 and intersectionData[1][1] < 1 and intersectionData[1][0] >= 0:
                    if obstacleDistance is not None:
                        obstacleDistance = min(obstacleDistance, intersectionData[1][0])
                    else:
                        obstacleDistance = intersectionData[1][0]
        if obstacleDistance is not None:
            obstacleDistance *= self.range
        return obstacleDistance

    def _calculateDirectionalVectors(self):
        # rangeVector starts from sensor location and goes till sensor range
        self.rangeVectorNormalized = np.array([cos(self.orientation), sin(self.orientation)])
        self.rangeVector = self.range * self.rangeVectorNormalized
        # perpendicular to rangeVectors
        self.crossVectorNormalized = np.array([-sin(self.orientation), cos(self.orientation)])

    def _calculateDrawPoints(self):
        v1 = np.array(self.location)
        self.readingVector = self.reading * self.rangeVectorNormalized
        self.sensorSpread = self.reading * 0.05 * self.crossVectorNormalized
        v2 = v1 + self.readingVector + self.sensorSpread
        v3 = v1 + self.readingVector - self.sensorSpread
        self.vertices = np.array([v1, v2, v3])
