import argparse
import math
import os
import sys
import machine as mach
import transform as xfm
import primitive as prim
import objio
import stlio


def spur(radius, axle_radius, depth, twist):
    points1, indices1 = mach.helical_spur(radius, 3, depth, twist)
    points2, indices2 = prim.tube(axle_radius, radius - 1, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1

def ring(radius, depth, twist):
    points1, indices1 = mach.helical_internal(radius, 3, depth, twist) 
    points2, indices2 = prim.tube(radius + 1, radius + 5, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1


def planetary(sun_radius, ring_radius, planet_axle_radius, sun_axle_radius, depth, twist, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    sun_teeth = mach.gear_wheel(sun_radius, 3, 0, -twist)
    planet_radius = (ring_radius - sun_radius)/2
    planet_teeth = mach.gear_wheel(planet_radius, 3, 0, twist)
    
    ring_teeth = mach.internal_gear(ring_radius, 3, 0, twist)
    required_ring_teeth = planet_teeth * 2 + sun_teeth

    print("RING_TEETH:")
    print("    ACTUAL:  ", ring_teeth)
    print("    REQUIRED:", required_ring_teeth)
    print("    {0} + {1} X 2".format(sun_teeth, planet_teeth))
    
    points1, indices1 = spur(sun_radius, sun_axle_radius, depth, twist=-twist) 
    points2, indices2 = spur(planet_radius, planet_axle_radius, depth, twist=twist)
    points3, indices3 = ring(ring_radius, depth, twist=twist)

    stlio.save(os.path.join(out_dir, "sun.stl"), points1, indices1)

    stlio.save(os.path.join(out_dir, "ring.stl"), points3, indices3)

    points2 = xfm.translate(points2, sun_radius + planet_radius, 0, 0)
    stlio.save(os.path.join(out_dir, "planet_1.stl"), points2, indices2)
        
    points2 = xfm.translate(points2, (sun_radius + planet_radius) * -2, 0, 0)
    stlio.save( os.path.join( out_dir, "planet_2.stl"), points2, indices2)

    points2 = xfm.translate(points2, sun_radius + planet_radius, 0, 0)
    points2 = xfm.translate(points2, 0, sun_radius + planet_radius,  0)
    stlio.save(os.path.join( out_dir, "planet_3.stl"), points2, indices2)
    
    points2 = xfm.translate(points2, 0, (sun_radius + planet_radius) * -2,  0)
    stlio.save(os.path.join(out_dir, "planet_4.stl"), points2, indices2)


def parse_args():
    """
    set configuration from cmdline
    """
    parser = argparse.ArgumentParser(
        prog="planetary",
        description="Build a speed reducing gear cluster"
    )

    parser.add_argument(
        "--sun-radius",
        type=float,
        default=7,
        dest="sun_radius",
        help="amount of speed reduction in a single stage",
    )

    parser.add_argument(
        "--ring-radius",
        type=float,
        default=35.7,
        dest="ring_radius",
        help="total number of stages",
    )

    parser.add_argument(
        "--twist",
        type=float,
        default=0.0,
        dest="twist",
        help="angle of twist for helical gears",
    )

    parser.add_argument(
        "--planet-axle-radius",
        type=float,
        default=11.15,
        dest="planet_axle_radius",
        help="radius of inner axle",
    )

    parser.add_argument(
        "--sun-axle-radius",
        type=float,
        default=2.6,
        dest="sun_axle_radius",
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
        "--directory",
        type=str,
        default="/var/tmp/assembly",
        dest="out_dir",
        help="output_directory",
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    planetary(
        args.sun_radius, 
        args.ring_radius, 
        args.planet_axle_radius, 
        args.sun_axle_radius, 
        args.depth, 
        args.twist, 
        args.out_dir)
    


