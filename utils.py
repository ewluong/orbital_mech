import math

def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def subtract(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def scale(v, scalar):
    return (v[0] * scalar, v[1] * scalar)

def magnitude(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)

def normalize(v):
    mag = magnitude(v)
    if mag == 0:
        return (0, 0)
    return (v[0] / mag, v[1] / mag)

def distance(v1, v2):
    return magnitude(subtract(v1, v2))
