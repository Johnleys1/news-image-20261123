"""Copy the pre-rendered front-page image to the grader's output folder.

Standard library only: the grader runs python3.13 with nothing installed,
so this program uses no third-party packages.
"""

import os

here = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
os.makedirs(dest_dir, exist_ok=True)

with open(os.path.join(here, "entry.png"), "rb") as source:
    picture = source.read()
with open(os.path.join(dest_dir, "entry.png"), "wb") as target:
    target.write(picture)
