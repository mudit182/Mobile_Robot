import numpy as np
from math import radians
from myMathFunctions import rotationMatrix2D
from state import CarState
from behaviors import GTG, AO, AOGTG, FW, NoFW, Full
from sensor import Sensor


class Car:
    def __init__(self, initialState, goal):
        self.state = CarState(initialState["type"], initialState["size"], initialState["location"],
                              initialState["orientation"], initialState["speed"], initialState["angularSpeed"], goal)
        self._calculateVertices()

        self._setLimits()
        self._loadSensors()
        self._loadBehaviors()
        self.event = "None"
        self.currentMode = "Start"

    def see(self, obstacles):
        for sensor in self.sensors:
            sensor.read(obstacles)

    def run(self, timeElapsed):
        self.eventCheck()
        # self.behaviors["GTG"].execute(self, timeElapsed)
        # self.behaviors["AO"].execute(self, timeElapsed)
        #   self.behaviors["AOGTG"].execute(self, timeElapsed)
        # self.behaviors["FW"].execute(self, timeElapsed)
        # self.behaviors["NoFW"].execute(self, timeElapsed)
        self.behaviors["Full"].execute(self, timeElapsed)

    def eventCheck(self):
        self.previousEvent = self.event

        if self.isColliding:
            self.event = "Collision"
        elif self.state.atGoal():
            self.event = "At Goal"
        elif self._sensorsActive():
            if self._sensorsCritical():
                self.event = "Unsafe"
            elif self.event == "Unsafe":
                self.event = "Safe"
            else:
                self.event = "At Obstacle"
        elif self.event == "Unsafe" or self.event == "At Obstacle":
            self.event = "Obstacle Cleared"
        else:
            self.event = "None"

        if not self.previousEvent == self.event:
            print("Event =", self.event)

    def _calculateVertices(self):
        w = self.state.size[0] / 2
        h = self.state.size[1] / 2
        corners = np.array([[-w, -h], [-w, h], [w, h], [w, -h]])
        rotMtx = rotationMatrix2D(self.state.orientation)
        self.vertices = [(np.array(rotMtx.dot(corner))[0] + self.state.location) for corner in corners]

    def _loadSensors(self):
        self.sensors = []
        for i in range(5):
            sensor = Sensor(i + 1, 100, radians(90 - i * 45), self)
            self.sensors.append(sensor)

    def _setLimits(self):
        self.maxAcceleration = 30
        self.maxBreaking = -60
        self.maxAngularSpeed = radians(120)
        self.isColliding = False

    def _loadBehaviors(self):
        self.behaviors = {}
        self.behaviors["GTG"] = GTG()
        self.behaviors["AO"] = AO()
        self.behaviors["AOGTG"] = AOGTG()
        self.behaviors["FW"] = FW()
        self.behaviors["NoFW"] = NoFW()
        self.behaviors["Full"] = Full()

    def _sensorsActive(self):
        active = False
        for sensor in self.sensors:
            if sensor.active:
                active = True
        return active

    def _sensorsCritical(self):
        self.criticalReading = 40
        return True if self._closestSensorReading() < self.criticalReading else False

    def _closestSensorReading(self):
        reading = self.sensors[0].range
        for sensor in self.sensors:
            reading = min(reading, sensor.reading)
        return reading
