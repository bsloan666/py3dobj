import machine as mach
import transform as xfm
import primitive as prim


def spur(radius, axle_radius, depth, twist):
    points1, indices1 = mach.twisted_spur(radius, 3, depth, twist, 0)
    points2, indices2 = prim.tube(axle_radius, radius - 1, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1

def bevel_spur(radius, axle_radius, depth, twist):
    points1, indices1 = mach.twisted_spur(radius, 6, depth, twist, (radius - depth)/radius)
    points2, indices2 = prim.conical_bushing(radius - 2, radius - (depth + 1.5), axle_radius, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1


def ring(radius, depth, twist):
    points1, indices1 = mach.twisted_internal(radius, 3, depth, twist) 
    points2, indices2 = prim.tube(radius + 1, radius + 5, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1


def reducer(ratio, minor_radius, axle_radius, depth, flip, twist):

    points1, indices1 = spur(minor_radius, 3, depth, twist)

    points2, indices2 = spur(minor_radius/ratio, 3, depth, twist=twist)

    if flip:
        points2 = xfm.translate(points2, 0, 0, depth)
    else:    
        points1 = xfm.translate(points1, 0, 0, depth)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    points2, indices2 = prim.tube(axle_radius, minor_radius - 1, depth, 64)

    points3, indices3 = prim.tube(
        axle_radius, minor_radius/ratio - 1, depth, 64)

    if flip:
        points3 = xfm.translate(points3, 0, 0, depth)
    else:
        points2 = xfm.translate(points2, 0, 0, depth)

    points2, indices2 = xfm.merge(points2, indices2, points3, indices3)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1


