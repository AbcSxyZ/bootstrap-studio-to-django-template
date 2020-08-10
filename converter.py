#!/usr/bin/env python3

from bss_converter import TagConverter
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("syntax error", file=sys.stderr)
        exit(1)
