import h5py
import numpy

data = numpy.zeros((512, 512), dtype=numpy.uint16)

with h5py.File("data.h5", "w") as f:
    d = f.create_dataset(
        "data",
        dtype=numpy.uint16,
        shape=(512, 512, 512),
        chunks=(1, 512, 512),
        compression="gzip",
    )
    for j in range(512):
        data[:, :] = j
        d[j] = data

    # now create a couple of virtual data sets pointing into this data from one
    # source data set which corresponds to the whole volume
    source = h5py.VirtualSource(".", "data", shape=(512, 512, 512))
    for j in range(2):
        layout = h5py.VirtualLayout(shape=(256, 512, 512), dtype=numpy.uint16)
        layout[:, :, :] = source[j * 256 : (j + 1) * 256]
        _ = f.create_virtual_dataset(f"data{j}", layout, fillvalue=-1)
