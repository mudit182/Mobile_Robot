import numpy as np
from math import radians, cos, sin, atan2


def angleRegular(angle):
    return atan2(sin(angle), cos(angle))


def rotationMatrix2D(angle):
    return np.matrix([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])


def vectorNorm(vector):
    return np.linalg.norm(np.array(vector))


def normalizeVector(vector):
    return vector / vectorNorm(vector)


def isColliding(obj1Points, obj2Points):
    # List points in correct order:
    #  shapes are considered as if drawn from first point to the next by a straight line,
    #  and that point joined to the one after that with another line, etc,
    #  until final point is joined to the first point
    colliding = True
    for i in range(len(obj1Points)):
        if colliding is True:
            j = i + 1 if not i == len(obj1Points) - 1 else 0
            side = np.array(obj1Points[i]) - np.array(obj1Points[j])
            # getNormalvector
            projectionAxis = normalizeVector(np.array(rotationMatrix2D(radians(90)).dot(side))[0])
            # project points of obj1 and get max and min
            obj1Projections = [np.array(point).dot(projectionAxis) for point in obj1Points]
            obj2Projections = [np.array(point).dot(projectionAxis) for point in obj2Points]
            if max(obj1Projections) > max(obj2Projections):
                if min(obj1Projections) > max(obj2Projections):
                    colliding = False

    for i in range(len(obj2Points)):
        if colliding is True:
            j = i + 1 if not i == len(obj2Points) - 1 else 0
            side = np.array(obj2Points[i]) - np.array(obj2Points[j])
            projectionAxis = np.array(rotationMatrix2D(radians(90)).dot(side))[0]
            # project points of obj1 and get max and min
            obj1Projections = [np.array(point).dot(projectionAxis) for point in obj1Points]
            obj2Projections = [np.array(point).dot(projectionAxis) for point in obj2Points]
            if max(obj1Projections) > max(obj2Projections):
                if min(obj1Projections) > max(obj2Projections):
                    colliding = False

    return colliding


def intersection2Lines2D(linePoint1, lineVector1, linePoint2, lineVector2):
    # Both lines pass from their linePoints and are parrallel to their lineVectors
    # function returns [ [a,b] , [c,d] ]
    # [a,b] is intersection point - None if lines are parrallel
    # c is fraction of lineVector1 at intersection - c*Vector1 + linePoint1 = [a, b]
    # d is fraction of lineVector2 at intersection -  d*Vector2 + linePoint2 = [a, b]
    A = np.matrix([[lineVector1[0], -lineVector2[0]], [lineVector1[1], -lineVector2[1]]])
    b = np.array([linePoint2[0] - linePoint1[0], linePoint2[1] - linePoint1[1]])
    if not np.linalg.det(A) == 0:
        fracLineVectors = np.array((np.linalg.inv(A).dot(b)))[0].tolist()
        intersectionPoint = (np.array(linePoint1) + np.array(lineVector1) * fracLineVectors[0]).tolist()
    else:
        fracLineVectors = None
        intersectionPoint = None
    return [intersectionPoint, fracLineVectors]
