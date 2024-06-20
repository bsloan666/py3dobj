import math
import numpy as np


def gear_tooth(pitch, depth):
    points = []
    indices = []
    extent = pitch/2
    yextent = pitch/3
    chamfer = pitch/6
    slope = pitch/24

    for z in [0, depth]:
        points.append([-extent, -yextent - chamfer, z])
        points.append([-extent, -yextent, z])
        points.append([-extent + chamfer, -yextent + chamfer, z])
        points.append([-extent + chamfer + slope, yextent - chamfer * 2, z])
        points.append([-extent + chamfer * 2, yextent - chamfer, z])
        points.append([0, yextent - chamfer, z])
        points.append([chamfer - slope, yextent - chamfer * 2, z])
        points.append([chamfer, -yextent + chamfer, z])
        points.append([chamfer * 2, -yextent, z])
        points.append([extent, -yextent, z])
        points.append([extent, -yextent - chamfer, z])

    off = 11
    for idx in range(1, 11):
        indices.append([idx + off, idx + 1 + off, idx + 1, idx])

    indices.append([22, 12, 1, 11])

    indices.append([1, 2, 10, 11])
    indices.append([2, 3, 8, 9])
    indices.append([3, 4, 7, 8])
    indices.append([4, 5, 6, 7])

    indices.append([22, 21, 13, 12])
    indices.append([20, 19, 14, 13])
    indices.append([19, 18, 15, 14])
    indices.append([18, 17, 16, 15])

    return points, indices


def tube(radius1, radius2, depth, grain):
    points = []
    indices = []
    angle = math.pi * 2 / grain

    for index1 in range(grain + 1):
        angle1 = index1 * angle
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )

        pt1 = [radius1, 0, 0]
        pt2 = [radius1, 0, depth]
        pt3 = [radius2, 0, depth]
        pt4 = [radius2, 0, 0]

        points.extend([
            np.matmul(matrix, pt1),
            np.matmul(matrix, pt2),
            np.matmul(matrix, pt3),
            np.matmul(matrix, pt4)
        ])

        if len(points) >= 8:
            p1 = len(points) - 7
            p2 = p1 + 1
            p3 = p1 + 2
            p4 = p1 + 3
            p5 = p1 + 4
            p6 = p1 + 5
            p7 = p1 + 6
            p8 = p1 + 7
            indices.extend([
                (p1, p2, p6, p5),
                (p7, p6, p2, p3),
                (p8, p7, p3, p4),
                (p5, p8, p4, p1)
            ])

    return points, indices


def cylinder(radius, depth, grain, caps=True):
    points = []
    indices = []
    angle = math.pi * 2 / grain

    # cap centers
    points.extend([
        [0, 0, 0],
        [0, 0, depth]
    ])

    for index1 in range(grain + 1):
        angle1 = index1 * angle
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )
        pt1 = [radius, 0, 0]
        pt2 = [radius, 0, depth]

        points.extend([
            np.matmul(matrix, pt1),
            np.matmul(matrix, pt2),
        ])

        if len(points) >= 6:
            p3 = len(points) - 3
            p4 = p3 + 1
            p5 = p3 + 2
            p6 = p3 + 3
            indices.extend([
                (p3, p4, p6, p5),
            ])
            if caps:
                indices.extend([
                    (p4, 2, p6),
                    (p5, 1, p3),
                ])

    return points, indices


def cone(radius1, radius2, depth, grain, caps=True):

    points = []
    indices = []
    angle = math.pi * 2 / grain

    # cap centers
    points.extend([
        [0, 0, 0],
        [0, 0, depth]
    ])

    for index1 in range(grain + 1):
        angle1 = index1 * angle
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )
        pt1 = [radius1, 0, 0]
        pt2 = [radius2, 0, depth]

        points.extend([
            np.matmul(matrix, pt1),
            np.matmul(matrix, pt2),
        ])

        if len(points) >= 6:
            p3 = len(points) - 3
            p4 = p3 + 1
            p5 = p3 + 2
            p6 = p3 + 3
            indices.extend([
                (p3, p4, p6, p5),
            ])
            if caps:
                indices.extend([
                    (p4, 2, p6),
                    (p5, 1, p3),
                ])

    return points, indices


def taurus(radius1, radius2, grain, arc_degrees=360):
    points = []
    texcoords = []
    indices = []
    angle = math.pi * 2 / grain

    arc_steps = int(grain * arc_degrees/360)

    for index1 in range(arc_steps + 1):
        angle1 = index1 * angle
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )
        for index2 in range(grain + 1):
            angle2 = index2 * angle

            init_pt = np.array(
                [
                    math.sin(angle2) * radius2 - radius1,
                    0,
                    -math.cos(angle2) * radius2
                ]
            )

            fin_pt = np.matmul(matrix, init_pt)
            points.append(fin_pt)

            texcoords.append((index2/grain, index1/grain))
            this_index = len(points)
            ul_nabe = this_index - 1
            lr_nabe = this_index - (grain + 1)
            ll_nabe = lr_nabe - 1
            if index1 and index2:
                indices.append((ll_nabe, ul_nabe, this_index, lr_nabe))

    return points, indices, texcoords


def sphere(radius, grain, arc_degrees=360):
    points = []
    indices = []
    angle = math.pi * 2 / grain
    half_angle = angle / 2

    arc_steps = int(grain * arc_degrees/360)

    points.extend([
        [0, 0, -radius],
        [0, 0, radius]
    ])

    for index1 in range(arc_steps + 1):
        angle1 = index1 * angle
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )
        for index2 in range(1, grain):
            angle2 = index2 * half_angle

            init_pt = np.array(
                [
                    math.sin(angle2) * radius,
                    0,
                    -math.cos(angle2) * radius
                ]
            )

            fin_pt = np.matmul(matrix, init_pt)
            points.append(fin_pt)

    for index in range(len(points)):
        if index > grain + 2:
            indices.append((
                (index - (grain - 1)) - 1,
                (index - (grain - 1)),
                index,
                index - 1
            ))

    return points, indices


def box(width, height, depth):
    points = []
    indices = []

    points.extend([
        (0, 0, 0),
        (0, height, 0),
        (width, height, 0),
        (width, 0, 0),
        (0, 0, depth),
        (0, height, depth),
        (width, height, depth),
        (width, 0, depth),
    ])

    indices.extend([
        (1, 2, 3, 4),
        (8, 7, 6, 5),
        (5, 6, 2, 1),
        (4, 3, 7, 8),
        (2, 6, 7, 3),
        (5, 1, 4, 8),
    ])

    return points, indices
