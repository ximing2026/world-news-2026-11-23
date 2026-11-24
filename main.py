"""Copy the committed poster image to /output/entry.png.

The bounty entry is a single pre-rendered picture, entry.png, which
lives next to this script. Running the script simply places that file
at the required output location.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB


def check_source():
    """Return an error message if the source is not a valid small PNG."""
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        return "entry.png is %d bytes, over the 1 MiB limit" % size
    with open(SOURCE, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        return "entry.png does not start with the PNG magic bytes"
    return None


def main():
    problem = check_source()
    if problem is not None:
        print("error: " + problem, file=sys.stderr)
        sys.exit(1)
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    print("wrote", DEST)


if __name__ == "__main__":
    main()
