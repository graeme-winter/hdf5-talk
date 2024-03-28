import os
import sys

import h5py
import numpy


def h5zip(name, path):
    """Walk over path, storing the files found in the new HDF5 file name"""

    with h5py.File(name, "w") as f:

        for (dirpath, dirnames, filenames) in os.walk(path):
            groupname = dirpath.replace(path, "/")
            g = f[groupname]
            assert groupname in f
            for dirname in sorted(dirnames):
                g.create_group(dirname)
            for filename in sorted(filenames):
                data = numpy.fromfile(
                    os.path.join(dirpath, filename), dtype=numpy.uint8
                )
                g.create_dataset(filename, data=data, compression="gzip")


h5zip(sys.argv[1], sys.argv[2])
