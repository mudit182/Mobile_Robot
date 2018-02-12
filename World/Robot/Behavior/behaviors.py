# import numpy as np
from modes import ModeGTG, ModeAO, ModeAOGTG, ModeFW, ModeFWwGoal


class GTG:
    def __init__(self):
        self.Modes = {}
        self.Modes["GTG"] = ModeGTG()

    def execute(self, robot, timeElapsed):
        if robot.event == "Collision" or robot.event == "At Goal":
            robot.state.stopMoving()
        else:
            self.currentMode = self.Modes["GTG"]
            self.currentMode.execute(robot, timeElapsed)


class AO:
    def __init__(self):
        self.Modes = {}
        self.Modes["AO"] = ModeAO()

    def execute(self, robot, timeElapsed):
        if robot.event == "Collision":
            robot.state.stopMoving()
        else:
            self.currentMode = self.Modes["AO"]
            self.currentMode.execute(robot, timeElapsed)


class AOGTG:
    def __init__(self):
        self.Modes = {}
        self.Modes["AOGTG"] = ModeAOGTG()

    def execute(self, robot, timeElapsed):
        if robot.event == "Collision" or robot.event == "At Goal":
            robot.state.stopMoving()
        else:
            self.currentMode = self.Modes["AOGTG"]
            self.currentMode.execute(robot, timeElapsed)


class FW:
    def __init__(self):
        self.Modes = {}
        self.Modes["FW"] = ModeFW()

    def execute(self, robot, timeElapsed):
        if robot.event == "Collision":
            robot.state.stopMoving()
        else:
            self.currentMode = self.Modes["FW"]
            self.currentMode.execute(robot, timeElapsed)


class NoFW:
    def __init__(self):
        self.Modes = {}
        self.Modes["GTG"] = ModeGTG()
        self.Modes["AO"] = ModeAO()
        self.Modes["AOGTG"] = ModeAOGTG()

    def execute(self, robot, timeElapsed):
        if robot.event == "Collision" or robot.event == "At Goal":
            robot.state.stopMoving()
        else:
            if robot.event == "At Obstacle" or robot.event == "Safe":
                self.currentMode = self.Modes["AOGTG"]
            elif robot.event == "Unsafe":
                self.currentMode = self.Modes["AO"]
            else:
                self.currentMode = self.Modes["GTG"]
            self.currentMode.execute(robot, timeElapsed)


class Full:
    def __init__(self):
        self.Modes = {}
        self.Modes["GTG"] = ModeGTG()
        self.Modes["AO"] = ModeAO()
        self.Modes["AOGTG"] = ModeAOGTG()
        self.Modes["FW"] = ModeFWwGoal()

    def execute(self, robot, timeElapsed):
        if robot.event == "Collision" or robot.event == "At Goal":
            robot.state.stopMoving()
        else:
            if robot.currentMode == "Follow Wall" and self.currentMode.goodToExit and robot.state.progressMade is True:
                self.currentMode = self.Modes["GTG"]
            elif robot.currentMode == "Follow Wall":
                pass
            elif robot.currentMode == "Avoid Obstacles" or robot.currentMode == "Avoid Obstacles And Go To Goal" and robot.state.progressMade is False:
                self.currentMode = self.Modes["FW"]
            else:
                if robot.event == "At Obstacle" or robot.event == "Safe":
                    self.currentMode = self.Modes["AOGTG"]
                elif robot.event == "Unsafe":
                    self.currentMode = self.Modes["AO"]
                else:
                    self.currentMode = self.Modes["GTG"]

            self.currentMode.execute(robot, timeElapsed)
