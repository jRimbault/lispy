#!/usr/bin/env python3

# Hook for testing application

from os import path
import sys


lib = path.realpath(path.join(path.dirname(__file__), ".."))
sys.path.insert(0, lib)


if __name__ == "__main__":
    import lispy

    lispy.main(lispy.parse_args())
