import struct
import transform

def pack_floats(floats):
    for float_val in floats:
        # Pack the float as little-endian 32-bit
        return struct.pack('<f', float_val) 

def pack_ints(ints):
    for int_val in ints:
        # Pack the int as little-endian 32-bit
        return struct.pack('<i', int_val) 

def pack_shorts(shorts):
    for short_val in shorts:
        # Pack the short as little-endian 32-bit
        return struct.pack('<h', short_val) 

def save(fname, points, indices):
    """
    Save out a STL file
    """
    data = []
    triangle_count = 0
    for index in indices:
        if len(index) == 4:
            p1 = points[face[0] -1]
            p2 = points[face[1] -1]
            p3 = points[face[2] -1]
            p4 = points[face[3] -1]

            normal = transform.normal(p1, p2, p3)
            data.append(pack_floats(normal))
            data.append(pack_floats(p1))
            data.append(pack_floats(p2))
            data.append(pack_floats(p3))
            data.append(pack_shorts([0]))
            data.append(pack_floats(normal))
            data.append(pack_floats(p3))
            data.append(pack_floats(p4))
            data.append(pack_floats(p1))
            data.append(pack_shorts([0]))
            triangle_count += 2
        else:
            p1 = points[face[0] -1]
            p2 = points[face[1] -1]
            p3 = points[face[2] -1]

            normal = transform.normal(p1, p2, p3)
            data.append(pack_floats(normal))
            data.append(pack_floats(p1))
            data.append(pack_floats(p2))
            data.append(pack_floats(p3))
            data.append(pack_shorts([0]))
            triangle_count += 1

    data.insert(0, pack_ints([triangle_count]))
    data.insert(0, pack_ints([0] * 20))

    with open(fname, "wb") as handle:
        for packed in data:
            handle.write(packed)

def load(fname):
    """
    Load an stl file
    """
    pass
