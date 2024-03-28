import h5py
import numpy

data = numpy.zeros((512, 512, 512), dtype=numpy.uint16)

for j in range(512):
    data[j, :, :] = j

with h5py.File("data.h5", "w") as f:
    p = f.create_dataset("data", data=data, chunks=(1, 512, 512), compression="gzip")
