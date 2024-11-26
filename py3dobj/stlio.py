import struct
import transform

def pack_floats(floats):
    chunks = []
    for float_val in floats:
        # Pack the float as little-endian 32-bit
        chunks.append(struct.pack('<f', float_val)) 
    return chunks

def pack_ints(ints):
    chunks = []
    for int_val in ints:
        # Pack the int as little-endian 32-bit
        chunks.append(struct.pack('<i', int_val)) 
    return chunks

def pack_shorts(shorts):
    chunks = []
    for short_val in shorts:
        # Pack the short as little-endian 32-bit
        chunks.append(struct.pack('<h', short_val)) 
    return chunks

def save(fname, points, indices):
    """
    Save out a STL file
    """
    data = []
    triangle_count = 0
    # points = transform.scale(points, 0.001, 0.001, 0.001)
    for face in indices:
        if len(face) == 4:
            p1 = points[face[0] -1]
            p2 = points[face[1] -1]
            p3 = points[face[2] -1]
            p4 = points[face[3] -1]

            normal = transform.normal(p1, p2, p3)
            data.extend(pack_floats(normal))
            data.extend(pack_floats(p1))
            data.extend(pack_floats(p2))
            data.extend(pack_floats(p3))
            data.extend(pack_shorts([0]))
            data.extend(pack_floats(normal))
            data.extend(pack_floats(p3))
            data.extend(pack_floats(p4))
            data.extend(pack_floats(p1))
            data.extend(pack_shorts([0]))
            triangle_count += 2
        else:
            p1 = points[face[0] -1]
            p2 = points[face[1] -1]
            p3 = points[face[2] -1]

            normal = transform.normal(p1, p2, p3)
            data.extend(pack_floats(normal))
            data.extend(pack_floats(p1))
            data.extend(pack_floats(p2))
            data.extend(pack_floats(p3))
            data.extend(pack_shorts([0]))
            triangle_count += 1

    header = pack_ints([0 for _ in range(20)])
    tcount = pack_ints([triangle_count])

    with open(fname, "wb") as handle:
        for struct in header:
            handle.write(struct)
        for struct in tcount:
            handle.write(struct)
        for struct in data:
            handle.write(struct)

def load(fname):
    """
    Load an stl file
    """
    pass
