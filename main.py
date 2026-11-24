"""Copy the bundled poster image to the output directory.

The entry ships a single committed picture, ``entry.png``, sitting next
to this script. Running the program places a copy of it at
``/output/entry.png`` so the bounty harness can pick it up.
"""

import shutil
import sys
from pathlib import Path

OUTPUT_PATH = Path("/output/entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_SIZE_BYTES = 1_048_576  # 1 MiB


def check_source(source: Path) -> str | None:
    """Return an error message if the source is not a sane PNG."""
    try:
        size = source.stat().st_size
        with source.open("rb") as handle:
            header = handle.read(len(PNG_MAGIC))
    except OSError as exc:
        return f"cannot read {source}: {exc}"
    if header != PNG_MAGIC:
        return f"{source} does not start with the PNG magic bytes"
    if size > MAX_SIZE_BYTES:
        return f"{source} is {size} bytes, over the 1 MiB limit"
    return None


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.png"
    problem = check_source(source)
    if problem is not None:
        print(f"error: {problem}", file=sys.stderr)
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, OUTPUT_PATH)
    print(f"copied {source} -> {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
