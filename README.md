# HDF5: a Very Rough Guide

Exploring the HDF5 file, on disk, with standard tooling.

## Introduction

OK, so I got sucked into giving a presentation to the group on what is HDF5 etc. which I thought "OK fine how hard can that be?" and indeed it is not hard, however as soon as you want to delve deep it rapidly turns into a fractal rabbit hole. That is fine. You just have to have the rabbit hole marker at the top and warn people not to dig too deep.

I started digging.

## Elementary HDF5

The HDF5 file format specification and libraries were essentially a collection of tools to allow the storage and manipulation of data without building up the technical debt of everyone's local "dat file" implementation or abominations like TIFF. Instead we have a whole load of _different_ technical debt to consider as well as a whole load of new tools to learn.

In reality it is nowhere near that bad. If you are used to using `less text.dat` to find out what is in a file then you're going to have to upskill, but if you are in a world where e.g. 60 gigapixels is a _typical_ data set then you're already in upskill territory.

While people talk about HDF5 _files_ it is more realistic to describe them as _file systems_ since they have most of the key properties: the ability to store and organise many collections of data, to annotate them with metadata and to move them as a collection from one place to another. In addition, like file systems, internal links are possible such that one data set can be accessed by a range of routes.

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

I didn't say at all that this is _helpful_, though a swift `print("".join(map(chr, handle["CODE_OF_CONDUCT.md"])))` will print something useful.

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

Seriously, bad chunking can have a catastrophic performance impact on your program. Do not underestimate this. I would not recommend you actually allow this to run to completion as it will take _ages_. I did, and my computer regrets it as it took 11m20s.

The fact that the chunks are what are stored on disk allows a few opportunities for optimisation. For example, if you have a detector which captures frames and can perform the compression on the data array in flight, you could, in principle, write that in the correct location (with a few pointers to the compression) and never have the HDF5 library manipulate the bytes at all. This is _direct chunk write_ and is fundamental to the operation of our Eiger detectors and a lot of what allows us to collect data at 500 frames / second with a 16 megapixel detector.

### Working with Chunks

If chunks are the fundamental storage unit, how can we work directly with them? On the most trivial level, from a consumer perspective, we can get the location (i.e. byte offset) and size of every chunk within the file and read them:

```python
import h5py

with h5py.File("data.h5", "r") as f:
    p = f["data"]
    i = p.id
    n = i.get_num_chunks()
    for j in range(n):
        c = i.get_chunk_info(j)
        print(f"{j} => {c.byte_offset}:+{c.size}")
```

N.B. this is now using some of the lower level HDF5 APIs. This will in turn allow us to extract the chunk and decompress it for ourselves:

```python
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

    for j in range(n):
        _, c = i.read_direct_chunk((j, 0, 0))
        b = zlib.decompress(c)
        a = numpy.frombuffer(b, dtype=numpy.uint16)
        assert (a == j).all()

with open("data.h5", "rb") as f:
    for j, (off, size) in enumerate(off_size):
        f.seek(off)
        c = f.read(size)
        b = zlib.decompress(c)
        a = numpy.frombuffer(b, dtype=numpy.uint16)
        assert (a == j).all()
```

N.B. reading the [docs](https://api.h5py.org/h5d.html) may help. Why would we ever want to do this? In a nutshell, performance. HDF5 has a very rudimentary model of thread safety, namely it puts a mutex around everything and calls it thread safe. This is fine if you are a data scientist fiddling around with a Jupyter notebook in lieu of using Excel, but it can punish in a high performance computing environment. The reading of the compressed chunks in HDF5 can be _very_ fast, but if you let the library do the data handling for you then you are limited to only using one thread for that.

If you use "proper" threads and are willing to have a thread pool of decompressors then you can get some very good performance from the system. You will also have to know a little more about the data, but you can extract that from the HDF5 file. It is worth noting that the direct reading _without_ going via the HDF5 libraries is 100% thread safe and you could hit that across every CPU you have access to without problems: I would not feel confident saying the same about the direct chunk reading (though it is probably OK.)

> The HDF5 library is very good for data access, very poor for compression handling, be prepared to work with the raw data representation

Where are we? We have some idea now of how to save data to files and how to access it in a moderately graceful manner. This is the most trivial use case for HDF5 but also probably one of the most useful. There is far more we can do even with _this_ before we move on to the next steps.

> If you are using direct chunk read as above with `read_direct_chunk` or the underlying `C` library, or fetching the data yourself with the offset and size _you must_ apply all the correct decompression filters etc. as described below to make sense of the values which come out.

## Advanced 0: Compression Schemes

Over the years there have been any number of different data compression schemes created, some of which are lossless and others lossy: which you elect to use depends entirely on your use case, and which works best is a function of the properties of your data and your personal use of the word best, e.g. do you mean time to compress / decompress or the ratio? If your fundamental data have a low degree of entropy (i.e. in general the next datum can often be predicted from prior knowledge) then most compression schemes will work well. If, however, your data are highly variable i.e. it is hard to predict the coming bits from the previous ones then the data will usually compress poorly. In some cases some intermediate manipulation of the data may reduce the entropy, thus improving the compression.

For data from photon counting detectors - perhaps one of our biggest uses of HDF5 - the data typically have a fairly low entropy, since many of the pixels are "background" and have small numbers of photons, following a Poisson distribution (the rate constant for this is frequently less than 1.0). Therefore, despite the in memory representation of the data taking e.g. 16 bits / pixel most pixels have an entropy far below this, allowing compression by a number of means. Since the majority of the image is background e.g.:

![A diffraction image module](./module.png)

We can further reduce the entropy by re-arranging the bits before performing the compression. This bit shuffle operation works on a block of data (e.g. 4096 x `uint16_t` values) and performs a massive transpose, putting 4096 x LSB, then next least significant bit, ... up to the most significant bits. This will typically result in very long sequences of null bytes, which compress very well with run-length encoding schemes such as LZ4 and friends. For the Eiger, we therefore have a compression scheme of `bslz4` i.e. a bitshuffle filter and LZ4 compression, with the data considered as blocks of a relatively small size.

If you look at the actual _bytes_ of a bitshuffle / LZ4 compressed chunk you then see: 8 bytes for the final length of the uncompressed image, then 4 bytes which defines the block size of file image, after which we get the compressed `lz4` blocks which themselves start with a four-byte header defining the _compressed_ size of that block.

Why would anyone care about any of this? Performance. If we want to decompress the data _really_ fast we could write an implementation of decompression which unpacks and unshuffles every block concurrently because we know exactly the address in the array it needs to end up in. How could you ever have access to that degree of paralellism? FPGA or GPU.

### Accessing Compression

The standard HDF5 library build comes with ZLIB compression and others by default, but not `bslz4` - for this you need to get a plugin otherwise you may end up seeing

```
Ethics-Gradient i04-1-run3-ins :( [main] $ python3
Python 3.10.8 | packaged by conda-forge | (main, Nov 22 2022, 08:25:13) [Clang 14.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import h5py
>>> f = h5py.File("Insulin_6_2_000001.h5", "r")
>>> d = f["data"]
>>> i = d[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "h5py/_objects.pyx", line 54, in h5py._objects.with_phil.wrapper
  File "h5py/_objects.pyx", line 55, in h5py._objects.with_phil.wrapper
  File "/Users/graeme/git/dials/conda_base/lib/python3.10/site-packages/h5py/_hl/dataset.py", line 768, in __getitem__
    return self._fast_reader.read(args)
  File "h5py/_selector.pyx", line 376, in h5py._selector.Reader.read
OSError: Can't read data (can't open directory: /Users/graeme/git/dials/conda_base/lib/hdf5/plugin)
```

Adding the `hdf5plugin` package to your Python install, and `import hdf5plugin` will resolve this. Obviously, most of the discussion which brought us to here has been around performance so you are unlikely to be working in Python, so you can fetch the source code [from here](https://github.com/kiyo-masui/bitshuffle) and add this to your application: this is very straightforward.

> Aside on compression, values etc. - to humans the numbers 0, 1 and -1 are very similar however the symbols we use to represent those (i.e. the bits) are very different! These are `0x0000`, `0x0001` and `0xffff` respectively for unsigned shorts: this in turn can put a lot of entropy into the bitstream.

## Advanced 1: Virtual Data Sets

The HDF5 files as described above are a literal (if chunked) representation of the data as in memory: while this is completely reasonable it is not always as _flexible_ as we may want. For example, you may have data sets recorded in one stream which are correct but do not follow a "logical" structure e.g. if you take a sequence of data sets one after the other and save them sequentially: individual datasets may be a subset of the full. Equally, a modular detector could reasonably record to a number of parallel data streams that we may want to reconstruct into a single view: HDF5 offers opportunities to address all these cases.

### Accessing a Subset

The subset challenge is a simple one: wanting a dataset which is a view onto a subset of the larger data set, e.g. frames 1800-3599 from a total data set recorded from frames 0-3599. This could be made a little more complex if the images themselves are recorded as blocks of 1,000 frames (this is not an idle or artificial example, this is exactly how things work in MX.) In this case we have:

```
|  data 0  |  data 1  |  data 2  | ..3 |
0123456789 0123456789 0123456789 012345
|   dataset 1 / 2  |   dataset 2 / 2   |
```

The terminology used in the HDF5 libraries is to consider the former to be the virtual source, and the latter to be a virtual data set made from the sources. The "real" data in `data 0, 1` will contribute to dataset 1, whilst the remains of `data 1` and the whole of `data 2, 3` will make up dataset 2: this is a 1D exmaple (though the datasets could consist of multidimensional arrays) but it is perfectly legitimate to create different shape virtual data sets.

To look at the structure of a virtual data set is easiest from Python, though it is also straightforward to inspect with the HDF5 command line tools or read from C. For example, a real data set taken on i03 at Diamond could have 3,600 images referenced in `/entry/data/data` but these are spread across four files as mentioned above:

```python
import sys

import h5py

def vds(vds_file, dataset="/entry/data/data"):
    """Print the information about VDS for vdsfile/dataset"""

    f = h5py.File(vds_file, "r")
    d = f[dataset]
    v = d.virtual_sources()

    for _v in v:
        vspace, file_name, dset_name, src_space = _v
        vbounds = vspace.get_select_bounds()
        print(vbounds[0][0], vbounds[1][0], file_name, dset_name)


if __name__ == "__main__":
    vds(sys.argv[1])
```

This will print files and ranges contributing to the virtual data set. Creating the VDS requires first creating a `VirtualLayout` of a given shape and type, then populating this from `VirtualSource`s which contribute the actual data, before finally creating the actual virtual data set which includes the "fill" value for those array elements which are otherwise undefined.

> Practical comment: if you load data into a viewer and every pixel has value e.g. `-1` then it is probably missing the files with the real data

Simplest example is to take the code above which made a single large data set, then make two smaller data sets which reference it - these work by using a virtual source to represent the source and a layout to define the destination, with slicing used to define the joins. As such, you can merge an arbitrary number of input data sets into an arbitrary number of output data sets:

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

    # now create a couple of virtual data sets pointing into this data from one
    # source data set which corresponds to the whole volume
    source = h5py.VirtualSource(".", "data", shape=(512, 512, 512))
    for j in range(2):
        layout = h5py.VirtualLayout(shape=(256, 512, 512), dtype=numpy.uint16)
        layout[:, :, :] = source[j * 256 : (j + 1) * 256]
        _ = f.create_virtual_dataset(f"data{j}", layout, fillvalue=-1)
```

### Merging Into a Larger Data Set

The logic for using virtual data set to build one big data set from smaller ones is identical with the only distinction being the use of multiple sources and a single layout:

```python
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
```

### Virtual Data Sets and Chunks

The use of virtual data set is a very helpful abstraction, but it is _an abstraction_: for e.g. enabling generic image viewers to work with performance driven complex structures of data this is legitimate, but when you wish to read the same data with performace some abstraction must be broken, as behind the scenes there are a lot of `memcpy` operations being used to provide this.

This is most evident in the use of direct chunk read and write: this works only with the real underlying data file, not with any virtual data set, so before any direct chunk access can be performed the virtual data sets must be "unpacked" and the book-keeping performed by hand.

## Advanced 2: Concurrency

HDF5 is a commonly used file format in high performance environments, but the concurrency model is relatively prehistoric and often quite unhelpful, for instance either requiring the use of MPI or putting everything behind a mutex lock to prevent cache mangling. A flagship feature of HDF5 1.10 was the implementation of SWMR: single writer multiple reader, which allowed HDF5 files to be read by multiple clients concurrently with dataset writing (N.B. not with dataset creation, which requires locks.) This feature sounds fantastic, but is not without problems. In particular the HDF5 libraries to a lot of "clever" things under the hood which can have some interesting interactions with distributed file systems. Combining this with GPFS has, in the past, made for some interesting debugging opportunities, not least when having multiple readers all access the same HDF5 file over GPFS the _writing_ became slower, suggesting somewhere deep in the system there is still some file locking taking place. Concurrent reading can be absolutely fine, provided that the processes are in their own address spaces (i.e. multiprocessing not multithreading.) Using HDF5 with multithreading is best achieved by having a reader thread perform the file access / chunk reading then passing the chunks to multiple worker threads to unpack and work on.

N.B. because we are now talking about threads and concurrency and the author is from the dark ages, this example is in `C`:

```c
/* hello from 1990 - please compile with h5cc -o fast_hdf5_eiger_read.c  */

#include <hdf5.h>
#include <hdf5_hl.h>
#include <limits.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

/* global variables - necessary until I move the whole shebang into a class */

pthread_mutex_t hdf_mutex;

int n_jobs;
int job;

hid_t dataset, datasize;
hsize_t dims[3];

/* data structures to manage the work */

typedef struct chunk_t {
  char *chunk;
  size_t size;
  int index;
} chunk_t;

/* next() method will lock and read the next chunk from the file as needed */

chunk_t next() {
  uint32_t filter = 0;
  hsize_t offset[3], size;
  chunk_t chunk;

  pthread_mutex_lock(&hdf_mutex);

  offset[0] = job;
  offset[1] = 0;
  offset[2] = 0;
  job += 1;

  if (job > n_jobs) {
    pthread_mutex_unlock(&hdf_mutex);
    chunk.size = 0;
    chunk.chunk = NULL;
    chunk.index = 0;
    return chunk;
  }

  H5Dget_chunk_storage_size(dataset, offset, &size);
  chunk.index = offset[0];
  chunk.size = (int)size;
  chunk.chunk = (char *)malloc(size);

  H5DOread_chunk(dataset, H5P_DEFAULT, offset, &filter, chunk.chunk);
  pthread_mutex_unlock(&hdf_mutex);
  return chunk;
}

/* data structure to store the results */

pthread_mutex_t result_mutex;

void save_result(uint64_t *result) {
  pthread_mutex_lock(&result_mutex);

  /* save things here */

  pthread_mutex_unlock(&result_mutex);
}

/* stupid interface to worker thread as it must be passed a void * and return
   the same */

void *worker(void *nonsense) {

  /* allocate frame storage - uses global information which is configured
     before threads spawned */

  int size = dims[1] * dims[2];
  char *buffer = (char *)malloc(datasize * size);

  /* while there is work to do, do work */

  while (1) {
    chunk_t chunk = next();
    if (chunk.size == 0) {
      free(buffer);
      return NULL;
    }

    // perform work on chunk.chunk knowing size, data type etc.

    free(chunk.chunk);
  }
  return NULL;
}

int main(int argc, char **argv) {
  hid_t file, plist, space, datatype;
  H5D_layout_t layout;

  file = H5Fopen(argv[1], H5F_ACC_RDONLY, H5P_DEFAULT);
  dataset = H5Dopen(file, argv[2], H5P_DEFAULT);
  plist = H5Dget_create_plist(dataset);
  datatype = H5Dget_type(dataset);
  datasize = H5Tget_size(datatype);
  layout = H5Pget_layout(plist);

  printf("Element size %lld bytes\n", datasize);

  if (layout != H5D_CHUNKED) {
    printf("You will not go to space, sorry\n");
    H5Pclose(plist);
    H5Dclose(dataset);
    H5Fclose(file);
    return 1;
  }

  space = H5Dget_space(dataset);

  printf("N dimensions %d\n", H5Sget_simple_extent_ndims(space));

  H5Sget_simple_extent_dims(space, dims, NULL);

  for (int j = 0; j < 3; j++) {
    printf("Dimension %d: %lld\n", j, dims[j]);
  }

  /* set up global variables */

  job = 0;
  n_jobs = dims[0];

  /* allocate and spin up threads */

  int n_threads = 1;

  if (argc > 3) {
    n_threads = atoi(argv[3]);
  }

  pthread_t *threads;

  pthread_mutex_init(&hdf_mutex, NULL);
  pthread_mutex_init(&result_mutex, NULL);

  threads = (pthread_t *)malloc(sizeof(pthread_t) * n_threads);

  for (int j = 0; j < n_threads; j++) {
    pthread_create(&threads[j], NULL, worker, NULL);
  }

  for (int j = 0; j < n_threads; j++) {
    pthread_join(threads[j], NULL);
  }

  pthread_mutex_destroy(&hdf_mutex);
  pthread_mutex_destroy(&result_mutex);

  H5Sclose(space);
  H5Pclose(plist);
  H5Dclose(dataset);
  H5Fclose(file);

  return 0;
}
```

This does not do any useful work, just reads the files, however if you wanted to decompress them or so some analysis you could easily do so.

## Advanced 3: Internal and External Links

So far everything which has been described has had all the data in a single HDF5 file, with data in one place. Like file systems HDF5 also allows links within the file, either "hard" links which are a second reference to the same data or "soft" links, which are an alias for another _reference_ to the data. The latter of these also allows that referenced object to be in another file, and this will be accessed transparently: when combined with virtual data sets this can allow some very flexible data handling.

### Hard Links

Hard links are a second, equivalent, reference to an existing data set e.g.

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

    g = f.create_group("entry")
    h = g.create_group("data")
    h["data"] = d
```

Is our routine data set, but now with a link to the same data under `/entry/data/data` to keep the NeXus folks happy:

```
Grey-Area links :) [main] $ h5ls -rv data.h5/entry/data/data
Opened "data.h5" with sec2 driver.
entry/data/data          Dataset {512/512, 512/512, 512/512}
    Location:  1:800
    Links:     2
    Chunks:    {1, 512, 512} 524288 bytes
    Storage:   268435456 logical bytes, 272836 allocated bytes, 98387.11% utilization
    Filter-0:  deflate-1 OPT {4}
    Type:      native unsigned short
```

### Soft Links

A soft link is different: it will remember the _name_ of the target rather than the target data, so if you remove the target you will get a dangling link: it does not however require that the target _exists_ so you can make the link in anticipation of it existing:

```python
    h["data_link"] = h5py.SoftLink("/data")
```

Added to the end of the above script gives:

```
HDF5 "data.h5" {
DATASET "/entry/data/data_link" {
   DATATYPE  H5T_STD_U16LE
   DATASPACE  SIMPLE { ( 512, 512, 512 ) / ( 512, 512, 512 ) }
   DATA {
   (0,0,0): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
   (0,0,22): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
   (0,0,43): 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
```

etc. but will be explicit that this is a soft link with e.g. `h5ls`.

### External Links

Once you have the idea of a soft link there is no real requirement that this is in the same file as the original: you can very easily have this be a relative path to another file, viz:

```python
with h5py.File("data.nxs", "w") as f:
    g = f.create_group("entry")
    h = g.create_group("data")
    h["data"] = h5py.ExternalLink("data.h5", "/data")
```

This creates a second file, with the NeXus structure, pointing at the original data - this allows the data to come from a different source to the metadata, which is _very_ useful in a high performance data environment. Data can be transparently accessed as:

```python
Grey-Area links :) [main] $ python3
Python 3.10.10 | packaged by conda-forge | (main, Mar 24 2023, 20:17:34) [Clang 14.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import h5py
>>> f = h5py.File("data.nxs")
>>> d = f["/entry/data/data"]
>>> d.shape
(512, 512, 512)
```

## Metadata

One of the big selling points is that HDF5 is self-describing (which is obviously false) but you can annotate HDF5 files with dataset information (and groups) which may help the consumer of the data interpret the values recorded. The attributes are essentially a hash table (key / value pair; dictionary) associated with groups and datasets which can have arbitrary values stored in them, such as units, the source of the data or other "human readable" things which aid in the understanding.

```python
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
```

These are visible by looking with `h5ls -rvd data.h5 | less` or more usefully `h5dump -A data.h5`:

```
HDF5 "data.h5" {
GROUP "/" {
   DATASET "data" {
      DATATYPE  H5T_STD_U16LE
      DATASPACE  SIMPLE { ( 512, 512, 512 ) / ( 512, 512, 512 ) }
      ATTRIBUTE "author" {
         DATATYPE  H5T_STRING {
            STRSIZE H5T_VARIABLE;
            STRPAD H5T_STR_NULLTERM;
            CSET H5T_CSET_UTF8;
            CTYPE H5T_C_S1;
         }
         DATASPACE  SCALAR
         DATA {
         (0): "graeme-winter"
         }
      }
      ATTRIBUTE "creation-timestamp" {
         DATATYPE  H5T_STRING {
            STRSIZE H5T_VARIABLE;
            STRPAD H5T_STR_NULLTERM;
            CSET H5T_CSET_UTF8;
            CTYPE H5T_C_S1;
         }
         DATASPACE  SCALAR
         DATA {
         (0): "2024-03-28T15:25:18.937333"
         }
      }
      ATTRIBUTE "source" {
         DATATYPE  H5T_STRING {
            STRSIZE H5T_VARIABLE;
            STRPAD H5T_STR_NULLTERM;
            CSET H5T_CSET_UTF8;
            CTYPE H5T_C_S1;
         }
         DATASPACE  SCALAR
         DATA {
         (0): "attrs.py"
         }
      }
   }
}
}```

... etc. (many numbers follow). This is the essence of NeXus files, which build an ontology on top of HDF5 to allow data to be annotated (outside of scope here.)
