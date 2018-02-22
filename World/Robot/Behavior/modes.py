from math import cos, sin, atan2, radians
import numpy as np
from myMathFunctions import normalizeVector, angleRegular
from baseControllers import PID


class Stop:
    def __init__(self):
        self.type = "Stop"


class SpeedTurnController:
    def __init__(self, type):
        self.type = type

    def setSpeedController(self, Kp, Ki, Kd, desiredSpeed):
        self.desiredSpeed = desiredSpeed
        self.speedController = PID(Kp, Ki, Kd)

    def setOrientationController(self, Kp, Ki, Kd):
        self.orientationController = PID(Kp, Ki, Kd)

    def _initMode(self, robot):
        if not self.type == robot.currentMode:
            self.speedController.reset()
            self.orientationController.reset()
            robot.currentMode = self.type
            print("Mode =", self.type)

    def _calculateAcceleration(self, currentSpeed, timeElapsed, newDesiredSpeed=None):
        if newDesiredSpeed is not None:
            self.desiredSpeed = newDesiredSpeed
        speedError = self.desiredSpeed - currentSpeed
        self.acceleration = self.speedController.getRateOfChange(speedError, timeElapsed)

    def _calculateAngularSpeed(self, desiredOrientation, currentOrientation, timeElapsed):
        errorOrientation = desiredOrientation - currentOrientation
        errorOrientation = atan2(sin(errorOrientation), cos(errorOrientation))
        self.angularSpeed = self.orientationController.getRateOfChange(errorOrientation, timeElapsed)

    def _moveRobot(self, robot, acceleration, angularSpeed, timeElapsed):
        acceleration = min(robot.maxAcceleration, acceleration) if acceleration > 0 else max(robot.maxBreaking, acceleration)
        angularSpeed = min(robot.maxAngularSpeed, angularSpeed) if angularSpeed > 0 else max(-robot.maxAngularSpeed, angularSpeed)
        robot.state.update(acceleration, angularSpeed, timeElapsed)
        robot._calculateVertices()
        for sensor in robot.sensors:
            sensor.updateState(robot)


class ModeGTG(SpeedTurnController):
    def __init__(self):
        SpeedTurnController.__init__(self, "Go To Goal")
        self.setSpeedController(5, 0.1, 0, 50)
        self.setOrientationController(5, 0.1, 0.05)

    def execute(self, robot, timeElapsed):
        self._initMode(robot)
        self._calculateAcceleration(robot.state.speed, timeElapsed)
        desiredOrientation = self._getDesiredOrientation(robot.state.goal, robot.state.location)
        self._calculateAngularSpeed(desiredOrientation, robot.state.orientation, timeElapsed)
        self._moveRobot(robot, self.acceleration, self.angularSpeed, timeElapsed)

    def _getDesiredOrientation(self, goal, currentLocation):
        return atan2((goal - currentLocation)[1], (goal - currentLocation)[0])


class ModeAO(SpeedTurnController):
    def __init__(self):
        SpeedTurnController.__init__(self, "Avoid Obstacles")
        self.setSpeedController(5, 0.1, 0, 50)
        self.setOrientationController(20, 0.1, 0.05)

    def execute(self, robot, timeElapsed):
        self._initMode(robot)
        self._calculateAcceleration(robot.state.speed, timeElapsed)
        desiredOrientation = self._getDesiredOrientation(robot.sensors)
        self._calculateAngularSpeed(desiredOrientation, robot.state.orientation, timeElapsed)
        self._moveRobot(robot, self.acceleration, self.angularSpeed, timeElapsed)

    def _getDesiredOrientation(self, sensors):
        directionVector = np.array([0.0, 0.0])
        weights = np.array([0.5, 0.9, 1.0, 0.9, 0.5])
        for i in range(len(sensors)):
            directionVector += sensors[i].rangeVectorNormalized * (sensors[i].reading) * weights[i]
        return atan2(directionVector[1], directionVector[0])


class ModeAOGTG(SpeedTurnController):
    def __init__(self):
        SpeedTurnController.__init__(self, "Avoid Obstacles And Go To Goal")
        self.setSpeedController(5, 0.1, 0, 30)
        self.setOrientationController(20, 0.1, 0.05)

        # alpha determines weightage of goal vs avoid obstacle direction
        self.alpha = 0.1

    def execute(self, robot, timeElapsed):
        self._initMode(robot)
        self._calculateAcceleration(robot.state.speed, timeElapsed)
        desiredOrientation = self._getDesiredOrientation(robot.state, robot.sensors)
        self._calculateAngularSpeed(desiredOrientation, robot.state.orientation, timeElapsed)
        self._moveRobot(robot, self.acceleration, self.angularSpeed, timeElapsed)

    def _getDesiredOrientation(self, state, sensors):
        goalDirVec = self._getGoalDirectionVector(state.goal, state.location)
        aODirVec = self._getAvoidObstacleDirectionVector(sensors)
        combinedDirVec = self.alpha * goalDirVec + (1 - self.alpha) * aODirVec
        return atan2(combinedDirVec[1], combinedDirVec[0])

    def _getGoalDirectionVector(self, goal, currentLocation):
        return normalizeVector(goal - currentLocation)

    def _getAvoidObstacleDirectionVector(self, sensors):
        directionVector = np.array([0.0, 0.0])
        weights = np.array([0.5, 0.9, 1.0, 0.9, 0.5])
        for i in range(len(sensors)):
            directionVector += sensors[i].rangeVectorNormalized * (sensors[i].reading) * weights[i]
        return normalizeVector(directionVector)


class ModeFW(SpeedTurnController):
    def __init__(self):
        SpeedTurnController.__init__(self, "Follow Wall")
        self.setSpeedController(5, 0.1, 0, 30)
        self.setOrientationController(5, 0.01, 0.01)
        self.alpha = 0.99
        self.followSide = "left"
        self.wallDistance = 60

    def execute(self, robot, timeElapsed):
        self._initMode(robot)
        self._calculateAcceleration(robot.state.speed, timeElapsed)
        self.angularSpeed = 0
        if robot._sensorsActive():
            desiredOrientation = self._getDesiredOrientation(robot.state.location, robot.sensors)
            self._calculateAngularSpeed(desiredOrientation, robot.state.orientation, timeElapsed)
        self._moveRobot(robot, self.acceleration, self.angularSpeed, timeElapsed)

    def _getDesiredOrientation(self, robotLocation, sensors):
        self._followCorrectSide(sensors)
        self._determineWallParallel(sensors)
        self._determineWallPerpendicular(robotLocation)
        combinedVec = self.alpha * self.wallParallelNormalized + (1 - self.alpha) * self.wallPerpendicularNormalized
        return atan2(combinedVec[1], combinedVec[0])

    def _followCorrectSide(self, sensors):
        if self.followSide == "left":
            sensorBegin = 0
        if self.followSide == "right":
            sensorBegin = 2
        correctSide = False
        for i in range(sensorBegin, sensorBegin + 3):
            if sensors[i].active is True:
                correctSide = True
        if correctSide is False:
            self.followSide = "right" if self.followSide == "left" else "left"

    def _determineWallParallel(self, sensors):
        if self.followSide == "left":
            if sensors[2].reading < sensors[0].reading:
                chosen2 = 2
                if sensors[0].reading < sensors[1].reading:
                    chosen1 = 0
                else:
                    chosen1 = 1
            else:
                chosen1 = 0
                if sensors[2].reading < sensors[1].reading:
                    chosen2 = 2
                else:
                    chosen2 = 1
        if self.followSide == "right":
            if sensors[2].reading < sensors[4].reading:
                chosen2 = 2
                if sensors[4].reading < sensors[3].reading:
                    chosen1 = 4
                else:
                    chosen1 = 3
            else:
                chosen1 = 4
                if sensors[2].reading < sensors[3].reading:
                    chosen2 = 2
                else:
                    chosen2 = 3
        self.p1 = sensors[chosen1].location + sensors[chosen1].readingVector
        self.p2 = sensors[chosen2].location + sensors[chosen2].readingVector
        self.wallParallel = self.p2 - self.p1

    def _determineWallPerpendicular(self, robotLocation):
        self.wallParallelNormalized = normalizeVector(self.wallParallel)
        self.wallPerpendicular = (self.p1 - robotLocation) - (self.p1 - robotLocation).dot(self.wallParallelNormalized) * self.wallParallelNormalized
        self.wallPerpendicularNormalized = self.wallPerpendicular - self.wallDistance * normalizeVector(self.wallPerpendicular)


class ModeFWwGoal(ModeFW):
    def __init__(self):
        ModeFW.__init__(self)
        self.goodToExit = False

    def execute(self, robot, timeElapsed):
        ModeFW.execute(self, robot, timeElapsed)
        self._checkIfShouldExit(robot)

    def _checkIfShouldExit(self, robot):
        if robot._sensorsActive() is False:
            self.goodToExit = True
        else:
            orientationParWall = atan2(self.wallParallel[1], self.wallParallel[0])
            orientationGoal = atan2((robot.state.goal - robot.state.location)[1], (robot.state.goal - robot.state.location)[0])
            orientationNormWall = atan2(-self.wallPerpendicular[1], -self.wallPerpendicular[0])
            angleParWallToGoal = angleRegular(orientationGoal - orientationParWall)
            angleGoalToNormWall = angleRegular(orientationNormWall - orientationGoal)
            angleWallToGoalToNorm = angleRegular(angleParWallToGoal + angleGoalToNormWall)
            if abs(angleParWallToGoal) <= radians(90) and abs(angleGoalToNormWall) <= radians(90):
                if abs(angleWallToGoalToNorm) <= radians(90):
                    self.goodToExit = True
                else:
                    self.goodToExit = False
            else:
                self.goodToExit = False
