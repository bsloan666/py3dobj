def save(fname, points, indices, normals=None, texcoords=None):
    """
    Save out a Wavefront OBJ file
    """
    with open(fname, "w") as handle:
        for point in points:
            handle.write("v {0} {1} {2}\n".format(
                point[0], point[1], point[2]))

        if texcoords:
            for uv in texcoords:
                handle.write("vt {0} {1}\n".format(
                    uv[0], uv[1]))

            for index in indices:
                if len(index) == 4:
                    handle.write("f {0}/{0} {1}/{1} {2}/{2} {3}/{3}\n".format(
                        index[0], index[1], index[2], index[3]))
                else:
                    handle.write("f {0}/{0} {1}/{1} {2}/{2}\n".format(
                        index[0], index[1], index[2]))
        else:
            for index in indices:
                if len(index) == 4:
                    handle.write("f {0} {1} {2} {3}\n".format(
                        index[0], index[1], index[2], index[3]))
                else:
                    handle.write("f {0} {1} {2}\n".format(
                        index[0], index[1], index[2]))


def load(fname):
    """
    Load a Wavefront OBJ file
    """
    pass
