import os
import sys
import pickle


def convert_pickles(dirname):
    """
    Load all .pkl TimedWord files in dirname (except volume*.pkl)
    and write ASCII-format files s_000, s_001, ... into the same directory.
    """

    files = sorted(
        f for f in os.listdir(dirname)
        if f.endswith(".pkl") and not f.startswith("volume")
    )

    print(f"Found {len(files)} pickle files in {dirname}")

    for i, fname in enumerate(files):
        path = os.path.join(dirname, fname)

        # load TimedWord
        with open(path, "rb") as f:
            w = pickle.load(f)

        # convert to ASCII
        txt = w.ascii_format_thao()

        # output: s_000, s_001, ...
        outname = f"s_{i:03d}"
        outpath = os.path.join(dirname, outname)

        with open(outpath, "w") as g:
            g.write(txt)

        print(f"wrote {outpath}")


# ------------------------------------------------------------
# Runnable script mode
# ------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_pickles.py <dirname>")
        sys.exit(1)

    convert_pickles(sys.argv[1])
