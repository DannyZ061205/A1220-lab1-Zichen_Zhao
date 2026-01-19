# file_io.py
"""File I/O utilities for reading and encoding files."""

import os
import base64


def encode_file(path):
    """Read a file and encode its contents as a base64 string.

    Args:
        path: The file path to read and encode.

    Returns:
        A base64-encoded string representation of the file contents.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def list_files(dirpath):
    """List all files in a directory.

    Args:
        dirpath: The path to the directory to scan.

    Yields:
        A tuple of (filename, filepath) for each file in the directory.
    """
    for name in os.listdir(dirpath):
        path = os.path.join(dirpath, name)
        if os.path.isfile(path):
            yield name, path

