import os


def safe_join(base, filename):
    filename = os.path.normpath(filename)
    full_path = os.path.join(base, filename)

    if not full_path.startswith(os.path.abspath(base)):
        raise Exception("Path traversal detected")

    return full_path