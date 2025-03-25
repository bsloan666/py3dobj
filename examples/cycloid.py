import transform as xfm
import machine as mach
import primitive as prim
import objio  as obj
import stlio
import sys

if __name__ == "__main__":
    inner_params = (30, 4.5)
    outer_params = (30.75, 4.5)

    inner_teeth = mach.gear_wheel(*inner_params, 0)
    print("INNER_TEETH:", inner_teeth)
    points, indices = mach.gear_wheel(*inner_params, 5)
    stlio.save("/Users/bsloan/Desktop/cyc_inner.stl", points, indices)

    outer_teeth = mach.internal_gear(*outer_params, 0)
    print("OUTER_TEETH:", outer_teeth)
    points, indices = mach.internal_gear(*outer_params, 10)
    stlio.save("/Users/bsloan/Desktop/cyc_outer.stl", points, indices)

    points, indices = mach.gear_wheel(17, 3, 8)
    stlio.save("/Users/bsloan/Desktop/bot_gear2.stl", points, indices)

