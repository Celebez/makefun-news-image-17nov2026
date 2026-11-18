#!/usr/bin/env python3
"""Entrypoint for make.fun's news-image-20261117 bounty.

The program runs twice in a fresh sandbox. It copies the pre-rendered
1024x1024 PNG to /output/entry.png; the bytes are identical on both runs.
Standard library only.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT_DIR, "entry.png"))
