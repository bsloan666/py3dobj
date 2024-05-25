import math
import primitive as prim
import transform as xfm


def gear_wheel(radius, pitch, depth):
    """
    A "cog"
    Pitch determines compatibility with other gears
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.translate(new_points, 0, radius, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices, _ = xfm.merge(
            points, indices, [], new_points, new_indices, [])

    return points, indices


def internal_gear(radius, pitch, depth):
    """
    Inward facing teeth
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.translate(new_points, 0, -radius, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices, _ = xfm.merge(
            points, indices, [], new_points, new_indices, [])

    return points, indices
