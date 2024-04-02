import h5py
import numpy

data = numpy.zeros((512, 512), dtype=numpy.uint16)

with h5py.File("data.h5", "w") as f:
    d = f.create_dataset(
        "data",
        dtype=numpy.uint16,
        shape=(512, 512, 512),
        chunks=(1, 512, 512),  # N.B. this line is subtly different
        compression="gzip",
    )
    for j in range(512):
        data[:, :] = j
        d[j] = data

    g = f.create_group("entry")
    h = g.create_group("data")
    h["data"] = d

    h["data_link"] = h5py.SoftLink("/data")

with h5py.File("data.nxs", "w") as f:
    g = f.create_group("entry")
    h = g.create_group("data")
    h["data"] = h5py.ExternalLink("data.h5", "/data")
