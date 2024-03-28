# HDF5

Exploring the HDF5 file, on disk, with standard tooling.

## Introduction

OK, so I got sucked into giving a presentation to the group on what is HDF5 etc. which I thought "OK fine how hard can that be?" and indeed it is not hard, however as soon as you want to delve deep it rapidly turns into a fractal rabbit hole. That is fine. You just have to have the 🐰🕳 marker at the top and warn people not to dig too deep.

I started digging.

## Elementary HDF5

The HDF5 file format specification and libraries were essentially a collection of tools to allow the storage and manipulation of data without building up the technical debt of everyone's local "dat file" implementation or abominations like TIFF. Instead we have a whole load of _different_ technical debt to consider as well as a whole load of new tools to learn.

In reality it is nowhere near that bad. If you are used to using `less text.dat` to find out what is in a file then you're going to have to upskill, but if you are in a world where e.g. 60 gigapixels is a _typical_ data set then you're already in upskill territory.

While people talk about HSF5 _files_ it is more realistic to describe them as _file systems_ since they have most of the key properties: the ability to store and organise many collections of data, to annotate them with metadata and to move them as a collection from one place to another. In addition, like file systems, internal links are possible such that one data set can be accessed by a range of routes.
