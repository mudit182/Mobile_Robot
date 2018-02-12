import pygame
from math import degrees
from colors import *
import numpy as np


originCartesian = np.array([0, 0])
originOnScreen = np.array([400, 300])
scaleCartesianToScreen = 1


def cartesianToScreen(point):
    return np.array([originOnScreen[0] + point[0], originOnScreen[1] - point[1]])


class _ScreenObjects:
    def __init__(self):
        pass

    def _convertToScreenCoord(self, point):
        return cartesianToScreen(point)


class Circle(_ScreenObjects):
    def __init__(self, center, radius=20, color=TEAL):
        _ScreenObjects.__init__(self)
        self.center = self._convertToScreenCoord(center)
        self.radius = radius
        self.color = color

    def updateDraw(self, screen, center):
        self.center = center
        self.draw(screen)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)


class Polygon(_ScreenObjects):
    def __init__(self, pointList, color=MAROON):
        _ScreenObjects.__init__(self)
        self._setPointList(pointList)
        self.color = color

    def updateDraw(self, screen, pointList):
        self._setPointList(pointList)
        self.draw(screen)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.pointList)

    def _setPointList(self, pointList):
        self.pointList = []
        for point in pointList:
            self.pointList.append(self._convertToScreenCoord(point))


class Polygon2Colors(Polygon):
    def __init__(self, pointList, color1, color2=SEAGREEN1):
        Polygon.__init__(self, pointList, color1)
        self.color1 = color1
        self.color2 = color2

    def updateDraw(self, screen, pointList, colorDecider=False):
        self.color = self.color1 if colorDecider is True else self.color2
        Polygon.updateDraw(self, screen, pointList)


class ImageObj(_ScreenObjects):
    def __init__(self, imgPath, size, location, orientation):
        _ScreenObjects.__init__(self)
        # pygame.sprite.Sprite.__init__(self)
        # Setting car width and height
        self.width, self.height = size
        # loading image file and transforming sprite to correct car size
        self.originalImg = pygame.image.load(imgPath)
        self.nonRotatedImg = pygame.transform.scale(
            self.originalImg, (self.width, self.height))
        # Setting car location and orientation
        self.orientation = degrees(orientation)
        self.location = self._convertToScreenCoord(location)
        # Transforming sprite to given orientation
        self._rotateToOrientation()
        # Converting car location to pygame image location (self.rect) for drawing
        self._genRectForPygame()

    def updateDraw(self, screen, newLocation, newOrientation):
        self.update(newLocation, newOrientation)
        self.draw(screen)

    def update(self, newLocation, newOrientation):
        self.location = self._convertToScreenCoord(newLocation)
        self.orientation = degrees(newOrientation)
        self._rotateToOrientation()
        self._genRectForPygame()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def _rotateToOrientation(self):
        # rotating to correct orientation
        self.image = pygame.transform.rotate(
            self.nonRotatedImg, self.orientation)

    def _genRectForPygame(self):
        # converting location in terms of pygame variables
        self.rect = self.image.get_rect(center=self.location)


class Background:
    def __init__(self, imgPath, location):
        self.image = pygame.image.load(imgPath)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
