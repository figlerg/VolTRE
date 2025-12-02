import os
import pickle

# directory containing the .pkl files
dirname = "07_delta_sigma_24_split"   # change if needed

files = sorted(
    f for f in os.listdir(dirname)
    if f.endswith(".pkl")
)

words = []

for fname in files:
    path = os.path.join(dirname, fname)
    with open(path, "rb") as f:
        w = pickle.load(f)
        words.append(w)

for i, w in enumerate(words):
    print(f"[{i:03d}] {w}")

    # convert to ASCII format
    txt = w.ascii_format_thao()

    # output file name: s_i
    # outname = f"s_{i}"
    outname = f"s_{i:03d}"
    outpath = os.path.join(dirname, outname)

    # write the ASCII file
    with open(outpath, "w") as g:
        g.write(txt)
