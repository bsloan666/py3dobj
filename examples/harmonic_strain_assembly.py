import machine as mach
import primitive as prim
import transform as xfm
import objio

if __name__ == "__main__":
    points1, indices1 = prim.sinus_cog(28.5, 5, 360, 12, 0.8)
    points2, indices2 = prim.sinus_ring(32.5, 10, 360, 11.6129, 0.8)

    objio.save("../../Documents/models/obj/sinus_cog.obj", points1, indices1)
    objio.save("../../Documents/models/obj/sinus_ring.obj", points2, indices2)
