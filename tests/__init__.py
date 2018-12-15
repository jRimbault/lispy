from contextlib import contextmanager
import io
from os import path
import sys

sys.path.insert(0, path.realpath(path.join(path.dirname(__file__), "..")))


@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, io.StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out
