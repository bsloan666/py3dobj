import primitive as prim
import objio

if __name__ == "__main__":

    points2, indices2 = prim.tube(2.6, 24, 64, 10)
    objio.save("/var/tmp/tube.obj", points2, indices2)
