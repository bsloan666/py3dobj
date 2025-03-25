import argparse
import math
import os
import sys
import machine as mach
import transform as xfm
import primitive as prim
import stlio


def gear_with_axle(radius, axle_radius, depth):

    points1, indices1 = mach.gear_wheel(radius, 3, depth)
    points2, indices2 = prim.tube(axle_radius, radius - 1, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1

def save_part(radius, axle_radius, depth, out_fname):
    points, indices = gear_with_axle(radius, axle_radius, depth)
    stlio.save(out_fname, points, indices)

def parse_args():
    """
    set configuration from cmdline
    """
    parser = argparse.ArgumentParser(
        prog="gear_with_axle",
        description="Build a speed reducing gear cluster"
    )

    parser.add_argument(
        "--radius",
        type=float,
        default=12,
        dest="radius",
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

    parser.add_argument(
        "--out-file",
        type=str,
        default="/var/tmp/gear.stl",
        dest="out_file",
        help="Full path of output (stl) file",
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    save_part(
        args.radius, 
        args.axle_radius, 
        args.depth, 
        args.out_file)


