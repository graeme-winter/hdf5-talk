import h5py
import numpy

secret = numpy.array(numpy.zeros((1024, 1024)), dtype=numpy.uint8)

secret[511][:5] = (1, 2, 3, 4, 5)

with h5py.File("secret.h5", "w") as f:
    p = f.create_dataset("password", data=secret, chunks=(1, 1024), compression="gzip")
