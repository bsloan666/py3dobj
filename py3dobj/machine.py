import math
import primitive as prim
import transform as xfm


def gear_wheel(radius, pitch, depth, twist=0.0):
    """
    A "cog"
    Pitch determines compatibility with other gears
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    if depth == 0:
        return num_teeth

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.translate(new_points, 0, radius, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)
        new_points[-11:] = xfm.rotate(new_points[-11:], twist/radius, 2)

        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices


def internal_gear(radius, pitch, depth, twist=0.0):
    """
    Inward facing teeth
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    if depth == 0:
        return num_teeth

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.translate(new_points, 0, -radius, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)
        new_points[-11:] = xfm.rotate(new_points[-11:], twist/radius, 2)


        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices


def helical_spur(radius, pitch, depth, twist):
    """
    piecewise linear approximation of helical spur gear
    """
    points = []
    indices = []
    n_slabs = 16
    slab_size = depth/n_slabs

    for offset in range(16):
        points_temp, indices_temp = gear_wheel(radius, pitch, slab_size, twist=twist/n_slabs)
        points_temp = xfm.translate(points_temp, 0, 0, slab_size * offset)
        points, indices = xfm.merge(
            points, indices, points_temp, indices_temp)
        points = xfm.rotate(points, -twist/radius/n_slabs, 2)

    return points, indices


def helical_internal(radius, pitch, depth, twist):
    """
    piecewise linear approximation of helical spur gear
    """
    points = []
    indices = []
    n_slabs = 16
    slab_size = depth/n_slabs

    for offset in range(16):
        points_temp, indices_temp = internal_gear(radius, pitch, slab_size, twist=twist/n_slabs)
        points_temp = xfm.translate(points_temp, 0, 0, slab_size * offset)
        points, indices = xfm.merge(
            points, indices, points_temp, indices_temp)
        points = xfm.rotate(points, -twist/radius/n_slabs, 2)

    return points, indices


def face_gear(radius, pitch, depth):
    """
    Radial teeth on one face of disk
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    if depth == 0:
        return num_teeth

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.rotate(new_points, 90, 0)
        new_points = xfm.translate(new_points, 0, -radius + depth, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices
