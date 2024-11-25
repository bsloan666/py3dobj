import math
import numpy as np


def rotate(points, arc_degrees, axis_index):
    """
    rotate by some number of degrees around x, y, or z
    """
    deg_to_rad = math.pi / 180
    arc_rad = deg_to_rad * arc_degrees

    if axis_index == 0:
        matrix = np.array(
            [
                [1, 0, 0],
                [0, math.cos(arc_rad), -math.sin(arc_rad)],
                [0, math.sin(arc_rad), math.cos(arc_rad)],
            ]
        )
    elif axis_index == 1:
        matrix = np.array(
            [
                [math.cos(arc_rad), 0, math.sin(arc_rad)],
                [0, 1, 0],
                [-math.sin(arc_rad), 0, math.cos(arc_rad)],
            ]
        )
    elif axis_index == 2:
        matrix = np.array(
            [
                [math.cos(arc_rad), -math.sin(arc_rad), 0],
                [math.sin(arc_rad), math.cos(arc_rad), 0],
                [0, 0, 1],
            ]
        )

    new_points = []
    for point in points:
        new_points.append(np.matmul(matrix, point))

    return new_points


def translate(points, tx, ty, tz):
    """
    translate an object by xyz
    """
    result = []
    for point in points:
        result.append(
            (
                point[0] + tx,
                point[1] + ty,
                point[2] + tz,
            )
        )

    return result


def scale(points, sx, sy, sz):
    """
    translate an object by xyz
    """
    for point in points:
        point[0] *= sx
        point[1] *= sy
        point[2] *= sz

    return points


def merge(points1, indices1, points2, indices2):
    offset = len(points1)

    points1.extend(points2)

    for face in indices2:
        indices1.append([i + offset for i in face])

    return points1, indices1

def subtract(vec_a, vec_b):
    return [a - b for a, b in zip(vec_a, vec_b)]

def add(vec_a, vec_b):
    return [a + b for a, b in zip(vec_a, vec_b)]

def normal(p1, p2, p3):
    vec_v = subtract(p2 - p1)
    vec_w = subtract(p3 - p1)
    n_x = (vec_v[1] * vec_w[2]) - (vec_v[2] * vec_w[1])  
    n_y = (vec_v[2] * vec_w[0]) - (vec_v[0] * vec_w[2])  
    n_z = (vec_v[0] * vec_w[1]) - (vec_v[1] * vec_w[0])
    return [n_x, n_y, n_z]
