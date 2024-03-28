import h5py
import numpy

data = numpy.zeros((512, 256), dtype=numpy.uint16)

with h5py.File("data.h5", "w") as f:
    d = f.create_dataset(
        "data0",
        dtype=numpy.uint16,
        shape=(512, 512, 256),
        chunks=(1, 512, 256),
        compression="gzip",
    )
    for j in range(512):
        data[:, :] = j
        d[j] = data

    d = f.create_dataset(
        "data1",
        dtype=numpy.uint16,
        shape=(512, 512, 256),
        chunks=(1, 512, 256),
        compression="gzip",
    )
    for j in range(512):
        data[:, :] = j
        d[j] = data

    source0 = h5py.VirtualSource(".", "data0", shape=(512, 512, 256))
    source1 = h5py.VirtualSource(".", "data1", shape=(512, 512, 256))
    layout = h5py.VirtualLayout(shape=(512, 512, 512), dtype=numpy.uint16)
    layout[:, :, 0:256] = source0
    layout[:, :, 256:512] = source1
    _ = f.create_virtual_dataset(f"data", layout, fillvalue=-1)
