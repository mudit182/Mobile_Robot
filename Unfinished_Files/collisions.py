#  import numpy as np


class Collision:
    def __init__(self, worldSize, divisionsNumWidth=3, divisionsNumHeight=3):
        self.worldSize = worldSize
        self._createSpactialMap(divisionsNumWidth, divisionsNumHeight)

    def _createSpactialMap(self, divisionsNumWidth, divisionsNumHeight):
        self.spatialMap = {}
        divisionsWidth = [self.worldSize[0] * mark / divisionsNumWidth for mark in range(1, divisionsNumWidth)]
        divisionsHeight = [self.worldSize[1] * mark / divisionsNumHeight for mark in range(1, divisionsNumHeight)]
        for i in range(divisionsWidth):
            for j in range(divisionsHeight):
                pass
