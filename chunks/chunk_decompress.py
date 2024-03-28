import zlib

import h5py
import numpy

off_size = []

with h5py.File("data.h5", "r") as f:
    p = f["data"]
    i = p.id
    n = i.get_num_chunks()
    for j in range(n):
        c = i.get_chunk_info(j)
        off_size.append((c.byte_offset, c.size))

with open("data.h5", "rb") as f:
    for j, (off, size) in enumerate(off_size):
        f.seek(off)
        c = f.read(size)
        b = zlib.decompress(c)
        a = numpy.frombuffer(b, dtype=numpy.uint16)
        assert (a == j).all()
