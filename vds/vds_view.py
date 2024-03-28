import h5py
import sys


def vds(vds_file, dataset="/entry/data/data"):
    """Print the information about VDS for vdsfile/dataset"""

    f = h5py.File(vds_file, "r")
    d = f[dataset]

    # get all the virtual data sources
    v = d.virtual_sources()

    for _v in v:
        # for each source, get the mapping between the virtual space in
        # the VDS to the real file, real data set and real data array -
        # this could be used to read the real data
        vspace, file_name, dset_name, src_space = _v
        vbounds = vspace.get_select_bounds()
        print(vbounds[0][0], vbounds[1][0], file_name, dset_name)


if __name__ == "__main__":
    vds(sys.argv[1])
