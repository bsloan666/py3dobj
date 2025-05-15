import primitive as prim
import transform as xfm


def letter_s(major, minor):
    """
    Stylized letter "S"
    """
    points1, indices1 = prim.taurus(
       major, minor, 64, 270
    )
    points2, indices2 = prim.taurus(
       major, minor, 64, 270
    )
    points1 = xfm.rotate(points1, 90, 2)
    points2 = xfm.rotate(points2, -90, 2)

    points1 = xfm.translate(points1, 0, major, 0)
    points2 = xfm.translate(points2, 0, -major, 0)

    points1 = xfm.scale(points1, 1, 0.5, 1)
    points2 = xfm.scale(points2, 1, 0.5, 1)

    return xfm.merge(
        points1, indices1, points2, indices2)
