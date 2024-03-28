import datetime

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
    d.attrs["source"] = "attrs.py"
    d.attrs["author"] = "graeme-winter"
    d.attrs["creation-timestamp"] = datetime.datetime.today().isoformat()