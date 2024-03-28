import h5py

with h5py.File("secret.h5", "r") as f:
    p = f["password"]
    i = p.id
    n = i.get_num_chunks()
    for j in range(n):
        c = i.get_chunk_info(j)
        print(f"{j:04x} => [{c.byte_offset:06x}:{c.byte_offset + c.size:06x}]")
