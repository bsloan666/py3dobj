import machine as mach
import transform as xfm
import objio

if __name__ == "__main__":

    points1, indices1 = mach.gear_wheel(25, 3, 10)
    points2, indices2 = mach.internal_gear(26.5, 3, 10)

    points1, indices1 = xfm.merge(
        points1, indices1, points2, indices2)

    points2, indices2 = mach.face_gear(54, 3, 8)
    points1, indices1 = xfm.merge(
        points1, indices1, points2, indices2)

    objio.save("./gears.obj", points1, indices1)
