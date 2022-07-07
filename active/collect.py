"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from os import listdir, makedirs
from shutil import rmtree
import zipfile
import sys


def get_full_name(string_, directory_):
    """Finds the filename containing a given string in a given directory."""
    files, k = [], 0
    for file in listdir(directory_):
        if string_ in file:
            k += 1
            files.append(file)
    if k == 1:
        return files[0]
    if k == 0:
        sys.stderr.write(f"String occurs in no filename of this directory.")
    else:
        sys.stderr.write(f"String occurs in several filenames of this directory:\n")
        for filename in files:
            sys.stderr.write(f"> {filename}\n")


def get_jp2_names(product_, src_):
    """Finds the full names of the required bands and directories."""
    path = f"{src_}/{product_}/GRANULE"
    r10m = f"{path}/{listdir(path)[0]}/IMG_DATA/R10m"
    r20m = f"{path}/{listdir(path)[0]}/IMG_DATA/R20m"
    scl = get_full_name('SCL', r20m)
    b2 = get_full_name('B02', r10m)
    b3 = get_full_name('B03', r10m)

    return scl, b2, b3, r10m, r20m


def unzip(origin_path, destination_path):
    """Unzips a file from its origin path to a given destination path."""
    with zipfile.ZipFile(origin_path, 'r') as zip_ref:
        zip_ref.extractall(destination_path)


def clear(directory_, subdirectories_):
    """Resets a given directory."""
    for object_ in listdir(directory_):
        rmtree(f"{directory_}/{object_}")
    for subdirectory_ in subdirectories_:
        makedirs(f"{directory_}/{subdirectory_}")


if __name__ == '__main__':

    pass
