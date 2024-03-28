import h5py
import numpy

secret = numpy.array((1, 2, 3, 4, 5), dtype=numpy.uint16)

with h5py.File("secret.h5", "w") as f:
    p = f.create_dataset("password", data=secret, chunks=(5,))
