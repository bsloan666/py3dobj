import primitive as prim
import transform as xform
import stlio
import math
import numpy as np

def cylinder_with_hole(radius, depth, grain):
    points = []
    indices = []
    angle = math.pi * 2 / grain

    loop = []
    loop2 = []

    # cap centers
    points.extend([
        [0, 0, 0],
        [0, 0, depth]
    ])

    for index1 in range(grain + 1):
        angle1 = index1 * angle
        angle2 = math.pi/2 
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )
        matrix2 = np.array(
            [
                [math.cos(angle2), 0, math.sin(angle2)],
                [0, 1, 0],
                [-math.sin(angle2), 0, math.cos(angle2)],
            ]
        )
        pt1 = [radius, 0, 0]
        pt2 = [radius, 0, 0]
        pt3 = [radius, 0, 0]
        pt4 = [radius, 0, depth] 

        pt1 = np.matmul(matrix, pt1)
        pt2 = np.matmul(matrix, pt2)
        pt3 = np.matmul(matrix2, pt2)
        pt4 = np.matmul(matrix, pt4)

        zpos1 = depth/2 - pt3[2] * 1.2
        zpos2 = pt3[2] * 1.2  + depth/2
        if pt1[0] > 0:
            zpos1 = depth/2
            zpos2 = depth/2

        pt2 = [pt1[0], pt1[1], zpos1]
        pt3 = [pt1[0], pt1[1], zpos2]


        points.append(pt1)
        points.append(pt2)
        points.append(pt3)
        points.append(pt4)

      
        if pt1[0] < 0.0:
            loop.append(pt2)
            loop2.append(pt3)
        elif pt1[0] == 0.0:
            loop.append(pt2)

        if len(points) >= 10:
            p3 = len(points) - 7
            p4 = p3 + 1
            p5 = p3 + 4
            p6 = p3 + 5
            p7 = p3 + 2
            p8 = p3 + 3
            p9 = p3 + 6
            p10 = p3 + 7

            indices.extend([
                (p5, p6, p4, p3),
            ])
            indices.extend([
                (p9, p10, p8, p7),
            ])
            indices.extend([
                (p3, 1, p5),
            ])
            indices.extend([
                (p10, 2, p8),
            ])

   
    loop2.extend(list(reversed(loop)))
    loop2.insert(0, loop2[-1])
    loop2.append(loop2[1])

    loop2.pop(grain//2 + 1)
    points.extend(loop2)
    return points, indices

def cylinder_with_cope(radius, depth, grain):
    points = []
    indices = []
    angle = math.pi * 2 / grain
    loop = []
    # cap centers
    points.extend([
        [0, 0, 0],
    ])

    for index1 in range(grain + 1):
        angle1 = index1 * angle
        angle2 = math.pi/2 
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )
        matrix2 = np.array(
            [
                [math.cos(angle2), 0, math.sin(angle2)],
                [0, 1, 0],
                [-math.sin(angle2), 0, math.cos(angle2)],
            ]
        )
        pt1 = [radius, 0, 0]
        pt2 = [radius, 0, 0]
        pt3 = [radius, 0, 0]

        pt1 = np.matmul(matrix, pt1)
        pt2 = np.matmul(matrix, pt2)
        pt3 = np.matmul(matrix2, pt2)
        [pt3] = xform.rotate([pt3], 90, 2)
        [pt3] = xform.rotate([pt3], -90, 1)
        pt2 = [pt1[0], pt1[1], - abs(pt3[2]) + depth]

        points.extend([pt1, pt2])
        loop.append(pt2)

        if len(points) >= 5:
            p3 = len(points) - 3
            p4 = p3 + 1
            p5 = p3 + 2
            p6 = p3 + 3
            indices.extend([
                (p5, p6, p4, p3),
            ])
            indices.extend([
                (p3, 1, p5),
            ])

    points.extend(loop)
    return points, indices


def tee(post_radius, post_depth, cross_radius, cross_depth, grain):
    post_points, post_indices = cylinder_with_cope(post_radius, post_depth, 64)

    cross_points, cross_indices = cylinder_with_hole(cross_radius, cross_depth, 64) 

    cross_points = xform.rotate(cross_points, 90, 1)
    cross_points = xform.rotate(cross_points, 180, 0)
    post_points = xform.rotate(post_points, -90, 2)
    cross_points = xform.translate(cross_points, -cross_depth / 2, 0, post_depth * 1.1)

    points, indices = post_points, post_indices
    size_post = len(post_points)
    start_loop1 = size_post - 65
    size_cross = len(cross_points) 
    points, indices = xform.merge(post_points, post_indices, cross_points, cross_indices)

    for index in range(start_loop1, start_loop1 + grain):
        indices.append([index + 1, index + size_cross + 2, index + size_cross + 1, index])

    size = len(points)
    indices.append([size, size - 1, size - 62])
    return points, indices



if __name__ == "__main__":
    points, indices = tee(30, 60, 30, 120, 64)
    stlio.save("../../Documents/tee.stl", points, indices)
