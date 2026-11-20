"""make.fun entry for news-image-20261119 (Python 3.13, stdlib only).

The graded image is the committed entry.png beside this file. This
program copies it, byte for byte, into the output directory: /output
inside the grader, or $MAKEFUN_OUTPUT_DIR when run locally. Copying
fixed bytes means the grader's two runs always agree.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()
