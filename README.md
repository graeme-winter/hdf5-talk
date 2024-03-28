# HDF5

Exploring the HDF5 file, on disk, with standard tooling.

## Introduction

OK, so I got sucked into giving a presentation to the group on what is HDF5 etc. which I thought "OK fine how hard can that be?" and indeed it is not hard, however as soon as you want to delve deep it rapidly turns into a fractal rabbit hole. That is fine. You just have to have the 🐰🕳 marker at the top and warn people not to dig too deep.

I started digging.

## Elementary HDF5

The HDF5 file format specification and libraries were essentially a collection of tools to allow the storage and manipulation of data without building up the technical debt of everyone's local "dat file" implementation or abominations like TIFF. Instead we have a whole load of _different_ technical debt to consider as well as a whole load of new tools to learn.

In reality it is nowhere near that bad. If you are used to using `less text.dat` to find out what is in a file then you're going to have to upskill, but if you are in a world where e.g. 60 gigapixels is a _typical_ data set then you're already in upskill territory.

While people talk about HSF5 _files_ it is more realistic to describe them as _file systems_ since they have most of the key properties: the ability to store and organise many collections of data, to annotate them with metadata and to move them as a collection from one place to another. In addition, like file systems, internal links are possible such that one data set can be accessed by a range of routes.

We can prove HDF5 is a container / file system by using it as exactly that.

### Abusing HDF5 1: replace zip

A "zip" file is simply a container which includes the paths for a collection of files and the compressed bytes corresponding to those files. This can be trivialluy reproduced with HDF5 by using a little Python and `h5py`:

```python
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
                g.create_dataset(filename, data=data, compression="gzip", compression_opts=9)


h5zip(sys.argv[1], sys.argv[2])
```

This little script walks over a directory and all subdirectories, reading all the files and adding them as compressed data sets while building the same directory tree as HDF5 groups. For example, we can demonstrate this by fetching the Python source code from [the release page](https://www.python.org/downloads/release/python-31014/) and adding it as above to a HDF5 container:

```
tar xvfz Python-3.10.14.tgz
python3 h5zip.py Python-3.10.14.h5 Python-3.10.14
```

=>

```
Grey-Area python :) $ du -hs *
100M	Python-3.10.14
 39M	Python-3.10.14.h5
 26M	Python-3.10.14.tgz
```

Yes, it is not as efficient because we are compressing the files individually and there is the overhead of the HDF5 structure for a huge number of files however:

```
Grey-Area python :) $ h5ls -r Python-3.10.14.h5
/                        Group
/.editorconfig           Dataset {181}
/.readthedocs.yml        Dataset {338}
/CODE_OF_CONDUCT.md      Dataset {630}
/Doc                     Group
/Doc/Makefile            Dataset {8946}
/Doc/README.rst          Dataset {4872}
/Doc/about.rst           Dataset {1487}
/Doc/bugs.rst            Dataset {4819}
/Doc/c-api               Group
---8<----
/Tools/unittestgui/README.txt Dataset {556}
/Tools/unittestgui/unittestgui.py Dataset {18521}
/aclocal.m4              Dataset {22792}
/config.guess            Dataset {49348}
/config.sub              Dataset {35276}
/configure               Dataset {525012}
/configure.ac            Dataset {179099}
/install-sh              Dataset {15368}
/pyconfig.h.in           Dataset {46565}
/setup.py                Dataset {117089}
```

Yes, the files are all included and we can look at them easily:

```
Grey-Area python :) $ h5ls -rvd Python-3.10.14.h5/CODE_OF_CONDUCT.md
Opened "Python-3.10.14.h5" with sec2 driver.
CODE_OF_CONDUCT.md       Dataset {630/630}
    Location:  1:18872
    Links:     1
    Chunks:    {630} 630 bytes
    Storage:   630 logical bytes, 389 allocated bytes, 161.95% utilization
    Filter-0:  deflate-1 OPT {9}
    Type:      native unsigned char
    Data:
         35, 32, 67, 111, 100, 101, 32, 111, 102, 32, 67, 111, 110, 100, 117,
         99, 116, 10, 10, 80, 108, 101, 97, 115, 101, 32, 110, 111, 116, 101,
         32, 116, 104, 97, 116, 32, 97, 108, 108, 32, 105, 110, 116, 101, 114,
         97, 99, 116, 105, 111, 110, 115, 32, 111, 110, 10, 91, 80, 121, 116,
         104, 111, 110, 32, 83, 111, 102, 116, 119, 97, 114, 101, 32, 70, 111,
         117, 110, 100, 97, 116, 105, 111, 110, 93, 40, 104, 116, 116, 112, 115,
         58, 47, 47, 119, 119, 119, 46, 112, 121, 116, 104, 111, 110, 46, 111,
         114, 103, 47, 112, 115, 102, 45, 108, 97, 110, 100, 105, 110, 103, 47,
         41, 45, 115, 117, 112, 112, 111, 114, 116, 101, 100, 10, 105, 110, 102,
         114, 97, 115, 116, 114, 117, 99, 116, 117, 114, 101, 32, 105, 115, 32,
         91, 99, 111, 118, 101, 114, 101, 100, 93, 40, 104, 116, 116, 112, 115,
         58, 47, 47, 119, 119, 119, 46, 112, 121, 116, 104, 111, 110, 46, 111,
         114, 103, 47, 112, 115, 102, 47, 114, 101, 99, 111, 114, 100, 115, 47,
         98, 111, 97, 114, 100, 47, 109, 105, 110, 117, 116, 101, 115, 47, 50,
         48, 49, 52, 45, 48, 49, 45, 48, 54, 47, 35, 109, 97, 110, 97, 103, 101,
         109, 101, 110, 116, 45, 111, 102, 45, 116, 104, 101, 45, 112, 115, 102,
         115, 45, 119, 101, 98, 45, 112, 114, 111, 112, 101, 114, 116, 105, 101,
         115, 41, 10, 98, 121, 32, 116, 104, 101, 32, 91, 80, 83, 70, 32, 67,
         111, 100, 101, 32, 111, 102, 32, 67, 111, 110, 100, 117, 99, 116, 93,
         40, 104, 116, 116, 112, 115, 58, 47, 47, 119, 119, 119, 46, 112, 121,
         116, 104, 111, 110, 46, 111, 114, 103, 47, 112, 115, 102, 47, 99, 111,
         100, 101, 111, 102, 99, 111, 110, 100, 117, 99, 116, 47, 41, 44, 10,
         119, 104, 105, 99, 104, 32, 105, 110, 99, 108, 117, 100, 101, 115, 32,
         97, 108, 108, 32, 116, 104, 101, 32, 105, 110, 102, 114, 97, 115, 116,
         114, 117, 99, 116, 117, 114, 101, 32, 117, 115, 101, 100, 32, 105, 110,
         32, 116, 104, 101, 32, 100, 101, 118, 101, 108, 111, 112, 109, 101,
         110, 116, 32, 111, 102, 32, 80, 121, 116, 104, 111, 110, 32, 105, 116,
         115, 101, 108, 102, 10, 40, 101, 46, 103, 46, 32, 109, 97, 105, 108,
         105, 110, 103, 32, 108, 105, 115, 116, 115, 44, 32, 105, 115, 115, 117,
         101, 32, 116, 114, 97, 99, 107, 101, 114, 115, 44, 32, 71, 105, 116,
         72, 117, 98, 44, 32, 101, 116, 99, 46, 41, 46, 10, 10, 73, 110, 32,
         103, 101, 110, 101, 114, 97, 108, 44, 32, 116, 104, 105, 115, 32, 109,
         101, 97, 110, 115, 32, 116, 104, 97, 116, 32, 101, 118, 101, 114, 121,
         111, 110, 101, 32, 105, 115, 32, 101, 120, 112, 101, 99, 116, 101, 100,
         32, 116, 111, 32, 98, 101, 32, 42, 42, 111, 112, 101, 110, 42, 42, 44,
         32, 42, 42, 99, 111, 110, 115, 105, 100, 101, 114, 97, 116, 101, 42,
         42, 44, 32, 97, 110, 100, 10, 42, 42, 114, 101, 115, 112, 101, 99, 116,
         102, 117, 108, 42, 42, 32, 111, 102, 32, 111, 116, 104, 101, 114, 115,
         32, 110, 111, 32, 109, 97, 116, 116, 101, 114, 32, 119, 104, 97, 116,
         32, 116, 104, 101, 105, 114, 32, 112, 111, 115, 105, 116, 105, 111,
         110, 32, 105, 115, 32, 119, 105, 116, 104, 105, 110, 32, 116, 104, 101,
         32, 112, 114, 111, 106, 101, 99, 116, 46, 10, 10
```

I didn't say at all that this is _helpful_.

This does show some useful pointers on how to explore HDF5 files however: we see that the percent utilisation is above 100: this says that the data were compressed at about 1.6:1 ratio, which is to be expected for a small text file. Real scientific data, particularly when sparse, can compress much more.

More usefully: I want to look for a specific data set in this file:

```
Grey-Area hdf5-talk :) [main] $ h5ls -r /tmp/python/Python-3.10.14.h5 | grep subprocess
/Doc/library/asyncio-subprocess.rst Dataset {11673}
/Doc/library/subprocess.rst Dataset {59383}
/Lib/_bootsubprocess.py  Dataset {2675}
/Lib/asyncio/base_subprocess.py Dataset {8843}
/Lib/asyncio/subprocess.py Dataset {7405}
/Lib/subprocess.py       Dataset {84917}
/Lib/test/subprocessdata Group
/Lib/test/subprocessdata/fd_status.py Dataset {835}
/Lib/test/subprocessdata/input_reader.py Dataset {130}
/Lib/test/subprocessdata/qcat.py Dataset {159}
/Lib/test/subprocessdata/qgrep.py Dataset {253}
/Lib/test/subprocessdata/sigchild_ignore.py Dataset {757}
/Lib/test/test_asyncio/test_subprocess.py Dataset {26892}
/Lib/test/test_subprocess.py Dataset {160086}
/Modules/_posixsubprocess.c Dataset {37870}
```

Then I want to see how well `/Lib/test/test_subprocess.py` was compressed:

```
Grey-Area hdf5-talk :) [main] $ h5ls -rv /tmp/python/Python-3.10.14.h5/Lib/test/test_subprocess.py
Opened "/tmp/python/Python-3.10.14.h5" with sec2 driver.
Lib/test/test_subprocess.py Dataset {160086/160086}
    Location:  1:19728907
    Links:     1
    Chunks:    {10006} 10006 bytes
    Storage:   160086 logical bytes, 39648 allocated bytes, 403.77% utilization
    Filter-0:  deflate-1 OPT {9}
    Type:      native unsigned char
```

We had 4:1 compression, since the file is quite a lot larger: this is now the sort of thing you routinely do when handing HDF5 files.

### More Sensible

A more sensible (more typical) use is to store arrays of data with some metadata attached: an example could be images of a certain size and data type, in a stack (thus making a 3D array).

```python
import h5py
import numpy

data = numpy.zeros((512, 512, 512), dtype=numpy.uint16)

for j in range(512):
    data[j, :, :] = j

with h5py.File("data.h5", "w") as f:
    p = f.create_dataset("data", data=data, chunks=(1, 512, 512), compression="gzip")
```

This creates _in memory_ a 512x512x512 array of two byte unsigned integers i.e. 256 MB of data. then saves this to disk: the file on disk is efficiently stored thanks to the trivial `gzip` compression of constant values:

```
Grey-Area demo :) [main+1] $ h5ls -rv data.h5
Opened "data.h5" with sec2 driver.
/                        Grou
    Location:  1:96
    Links:     1
/data                    Dataset {512/512, 512/512, 512/512}
    Location:  1:800
    Links:     1
    Chunks:    {1, 512, 512} 524288 bytes
    Storage:   268435456 logical bytes, 272836 allocated bytes, 98387.11% utilization
    Filter-0:  deflate-1 OPT {4}
    Type:      native unsigned short
```

In creating the data set we also gave it some hints: we passed the data array but we also passed the size of a "chunk" - this is fundamental to the efficient consideration of how to use HDF5 files and will be considered next - the data _type_ from the Numpy array was also passed through so the reader knows how the compressed bytes in the file should be interpreted.

## Real HDF5

The real value in HDF5 comes from considering (i) complex file structures and (ii) data sets which are too large to efficiently hold in memory. The above example created the data set in memory then saved it to disk, defining the "chunk" size. This is not an ideal way to work as it means that the whole data set _was_ in memory, but is easy as a demo. We can find a better way to do this after discussing what chunks are.

### Chunks

In HDF5 terms a chunk is a usefully sized quantum of data, i.e. it is big enough to compress usefully, and to contain a meaningful subset of a data set, but small enough to fit into RAM and (usually) not need slicing. A typical example could be a diffraction image, an MCA spectrum or a timepoint from a (small) 3D simulation.

Within HDF5 the compression is performed on chunks, and the compressed chunks are what are written to disk in the HDF5 file. This means to read elements of that chunk the whole chunk needs to be read from disk and decompressed: this may be cached to allow neighbouring reads to be fairly efficient but that means that there _can_ be caching going on behind the scenes. This brings us to an important point:

> The HDF5 libraries may perform additional operations to be helpful

You need to be aware of this as it may well come back to bite you later.

Sensible chunk selection may have a significant impact on the performance of your application. This is best considered by demonstration, where we first create the data file above but this time we _do not_ create the entire thing in RAM, and instead allocate the data set and fill it a chunk at a time:

```python
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
```

This makes _precisely_ the same file as the example above (i.e. the bytes are identical) and takes 1.45s to run. If, instead, we were to chunk the data in the same size blocks but in an unhelpful direction it would take a lot longer to save the same data array:

```python
import h5py
import numpy

data = numpy.zeros((512, 512), dtype=numpy.uint16)

with h5py.File("data.h5", "w") as f:
    d = f.create_dataset(
        "data",
        dtype=numpy.uint16,
        shape=(512, 512, 512),
        chunks=(512, 1, 512), # N.B. this line is subtly different
        compression="gzip",
    )
    for j in range(512):
        data[:, :] = j
        d[j] = data
```

This small change means we now have to read, decompress, write a line, compress and write 512 times for every frame: you really _really_ don't want to be doing this. Gives us axiom 2:

> Yes there is abstraction but be aware what is happening under the hood.

Seriously, bad chunking can have a catastrophic performance impact on your program. Do not underestimate this.
