import transform as xfm
import machine as mach
import primitive as prim
import objio  as obj
import sys

if __name__ == "__main__":
    points, indices = mach.gear_wheel(44, 3.2, 10)
    obj.save(sys.argv[1], points, indices)


