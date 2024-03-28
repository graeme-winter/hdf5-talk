import h5py

with h5py.File("data.h5", "r") as f:
    p = f["data"]
    i = p.id
    n = i.get_num_chunks()
    for j in range(n):
        c = i.get_chunk_info(j)
        print(f"{j} => {c.byte_offset}:+{c.size}")
