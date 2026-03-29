import os

def safe_join(base, filename):
    filename = os.path.normpath(filename)

    full_path = os.path.join(base, filename)

    base = os.path.abspath(base)
    full_path = os.path.abspath(full_path)

    if not full_path.startswith(base):
        raise Exception("Path traversal detected")

    return full_path