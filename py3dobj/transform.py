import math
import numpy as np


def rotate(points, arc_degrees, axis_index):
    """
    rotate by some number of degrees around x, y, or z
    """
    deg_to_rad = math.pi / 180
    arc_rad = deg_to_rad * arc_degrees

    # z axis case
    matrix = np.array(
        [
            [math.cos(arc_rad), -math.sin(arc_rad), 0],
            [math.sin(arc_rad), math.cos(arc_rad), 0],
            [0, 0, 1],
        ]
    )
    if axis_index == 0:
        pass
    if axis_index == 1:
        pass

    new_points = []
    for point in points:
        new_points.append(np.matmul(matrix, point))

    return new_points


def translate(points, tx, ty, tz):
    """
    translate an object by xyz
    """
    for point in points:
        point[0] += tx
        point[1] += ty
        point[2] += tz

    return points


def scale(points, sx, sy, sz):
    """
    translate an object by xyz
    """
    for point in points:
        point[0] *= sx
        point[1] *= sy
        point[2] *= sz

    return points


def merge(points1, indices1, texcoords1, points2, indices2, texcoords2):
    offset = len(points1)

    points1.extend(points2)
    texcoords1.extend(texcoords2)

    for face in indices2:
        indices1.append([i + offset for i in face])

    return points1, indices1, texcoords1
