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
                    -math.cos(angle2) * radius2 - radius1
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