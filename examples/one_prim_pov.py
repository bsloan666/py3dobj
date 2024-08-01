import transform as xfm
import machine as mach
import primitive as prim
import povrayio  as pov
import sys

if __name__ == "__main__":
    points, indices = mach.gear_wheel(12, 3, 3)
    points2, indices2 = prim.taurus(30, 8, 128, 360)

    points2 = xfm.translate(points2, 0, 0, 20)

    points, indices = xfm.merge(
        points, indices, points2, indices2)
    points2, indices2 = prim.sphere(15, 128, 360)

    points2 = xfm.translate(points2, 0, 0, 80)

    points, indices = xfm.merge(
        points, indices, points2, indices2)
    pov.save(sys.argv[1], points, indices)


