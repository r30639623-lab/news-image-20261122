#!/usr/bin/env python3
"""Entry program for news-image-20261122 (stdlib only).

Copies the pre-rendered front page (news.png, drawn locally by render.py)
to $MAKEFUN_OUTPUT_DIR/entry.png. Deterministic by construction: a plain
file copy. Never writes into the repo (read-only on the grader).
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news.png")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
