def default_camera():
    return """
    camera {
        perspective
        location <0.0, 1.5, -32.0>
        direction <0, 0, 1>
        up y
        right x*1.77
        look_at <0.0, 0.5, 0.00>
    }
    """


def default_light():
    return """
    light_source {
        <10.00, 15.00, -20.00>
        color White
        area_light <5, 0, 0>, <0, 0, 5>, 5, 5
        adaptive 1
        jitter
    }
    """


def header():
    return """
    #version 3.7;

    global_settings { assumed_gamma 2.2 }

    #include "colors.inc"
    #include "textures.inc"
    #include "shapes.inc"
    #include "functions.inc"

    #declare rseed = seed(123);

    #default {
        pigment { White }
        finish {
            ambient .2
            diffuse .6
            specular .25
            roughness .1
        }
    }
    """


def triangulate_face(points, face):
    """
    given a set of points, indices and a face index,
    return that face as one or more povray mesh triangle objects
    """

    result = ""

    def format_triangle( p1, p2, p3):
        out_str = "  triangle { " 
        out_str += "<{0}, {1}, {2}>, ".format(p1[0], p1[1], p1[2]) 
        out_str += "<{0}, {1}, {2}>, ".format(p2[0], p2[1], p2[2]) 
        out_str += "<{0}, {1}, {2}>  ".format(p3[0], p3[1], p3[2]) 
        out_str += "}\n"
        return out_str

    result += format_triangle( 
        points[face[0] - 1],
        points[face[1] - 1],
        points[face[2] - 1],
    )

    if len(face) == 4:
        result += format_triangle( 
            points[face[0] - 1],
            points[face[2] - 1],
            points[face[3] - 1],
        )

    return result

def save(fname, points, indices, normals=None, texcoords=None):
    """
    Save out a povray mesh block file
    """
    with open(fname, "w") as handle:
        handle.write(header())
        handle.write(default_light())
        handle.write(default_camera())
        handle.write("mesh {\n")
        for index in indices:
            handle.write(triangulate_face(points, index))

        handle.write("}\n")

def load(fname):
    """
    Load a Wavefront OBJ file
    """
    pass
