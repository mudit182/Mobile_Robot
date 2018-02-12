import json
import numpy as np
from myMathFunctions import isColliding
from mobileRobot import Car


class World:
    def __init__(self):
        self._createEnvironment()
        self._createRobot()

    def update(self, timeElapsed):
        self.checkCollisions()
        self.car.see(self.obstacles)
        self.car.run(timeElapsed)

    def checkCollisions(self):
        collision = False
        for obstacle in self.obstacles:
            if isColliding(obstacle.vertices, self.car.vertices) is True:
                collision = True
        self.car.isColliding = collision

    def _createEnvironment(self):
        self.goal = np.array([-300, 100])
        self.obstacles = []
        try:
            with open('World/environment3.json', 'r') as file:
                environmentInfo = json.load(file)
        except Exception as e:
            print("Error! Obstacles.json file not read!")
            print(str(e))
            environmentInfo = None

        if environmentInfo is not None:
            for i in range(environmentInfo["obstacles count"]):
                ob = Obstacle(i + 1, np.array(environmentInfo["obstacles vertices"][i]))
                self.obstacles.append(ob)

            self.goal = np.array(environmentInfo["goal"])

    def _createRobot(self):
        carInitialState = {}
        try:
            with open('World/Robot/carStartState.json', 'r') as info:
                carInitialState = json.load(info)
        except Exception as e:
            print("Error! RobotStartState.json file not read!")
            print(str(e))

        self.car = Car(carInitialState, self.goal)


class Obstacle:
    def __init__(self, number, vertices):
        self.number = number
        self.vertices = np.array(vertices)
