import argparse
import math
import os
import sys
import machine as mach
import transform as xfm
import primitive as prim
import objio


def gear(teeth, axle_radius, depth):

    radius = 12
    while mach.internal_gear(radius, 3, 0) < 60:
        radius += 1
     
    points1, indices1 = mach.internal_gear(radius, 3, depth)

    points2, indices2 = mach.gear_wheel(minor_radius/ratio, 3, depth)

    points1 = xfm.translate(points1, 0, 0, depth)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    points2, indices2 = prim.tube(axle_radius, minor_radius - 1, depth, 64)

    points2 = xfm.translate(points2, 0, 0, depth)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    points2, indices2 = prim.tube(
        axle_radius, minor_radius/ratio - 1, depth, 64)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1


def assembly(ratio, repeats, minor_radius, axle_radius, depth):
    out_dir = "/var/tmp/assembly"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    height = depth
    for index in range(repeats):
        points, indices = reducer(ratio, minor_radius, axle_radius, depth)
        points = xfm.translate(points, 0, 0, (index + 1) * depth)
        if index % 2:
            points = xfm.translate(points, minor_radius + minor_radius / ratio, 0, 0)

        objio.save(
            os.path.join(
                out_dir, "reducer_{0}.obj".format(index)), points, indices)
        height += depth

    height += depth * 2
    points, indices = prim.cylinder(axle_radius - 0.1, height, 64)
    objio.save(os.path.join(out_dir, "axle_1.obj"), points, indices)
    points = xfm.translate(points, minor_radius + minor_radius / ratio, 0, 0)
    objio.save(os.path.join(out_dir, "axle_2.obj"), points, indices)
    points, indices = prim.tube(axle_radius, minor_radius / ratio, depth / 2, 64)
    points = xfm.translate(points, 0, 0, depth/2)
    objio.save(os.path.join(out_dir, "case_1.obj"), points, indices)
    points = xfm.translate(points, minor_radius + minor_radius / ratio, 0, 0)
    objio.save(os.path.join(out_dir, "case_2.obj"), points, indices)
    points = xfm.translate(points, 0, 0, (repeats + 1.5) * depth)
    objio.save(os.path.join(out_dir, "case_3.obj"), points, indices)
    points = xfm.translate(points, -(minor_radius + minor_radius / ratio), 0, 0)
    objio.save(os.path.join(out_dir, "case_4.obj"), points, indices)



def parse_args():
    """
    set configuration from cmdline
    """
    parser = argparse.ArgumentParser(
        prog="gearbox",
        description="Build a speed reducing gear cluster"
    )

    parser.add_argument(
        "--step-ratio",
        type=float,
        default=0.333333,
        dest="step_ratio",
        help="amount of speed reduction in a single stage",
    )

    parser.add_argument(
        "--repeats",
        type=int,
        default=4,
        dest="repeats",
        help="total number of stages",
    )

    parser.add_argument(
        "--minor-radius",
        type=float,
        default=12,
        dest="minor_radius",
        help="radius of smallest cog",
    )

    parser.add_argument(
        "--axle-radius",
        type=float,
        default=2.6,
        dest="axle_radius",
        help="radius of inner axle",
    )

    parser.add_argument(
        "--depth",
        type=float,
        default=6,
        dest="depth",
        help="thickness of single cog",
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    assembly(args.step_ratio, args.repeats, args.minor_radius, args.axle_radius, args.depth)
    
    total_speed_reduction = args.step_ratio ** args.repeats

    print("Total speed reduction is {0}".format(total_speed_reduction))

