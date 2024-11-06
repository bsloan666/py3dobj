import machine as mach
import primitive as prim
import transform as xfm
import objio

if __name__ == "__main__":
    points1, indices1 = prim.sinus_cog(26, 5, 360, 24, 2)
    points2, indices2 = prim.sinus_ring(32.5, 10, 360, 22.5, 2)

    objio.save("./gears1.obj", points1, indices1)
    objio.save("./gears2.obj", points2, indices2)
