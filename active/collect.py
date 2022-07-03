"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from os import listdir, makedirs
from shutil import rmtree
import zipfile
import sys


def find_string_in_directory(string_, directory_):

    files, k = [], 0
    for file in listdir(directory_):
        if string_ in file:
            k += 1
            files.append(file)
    if k == 1:
        return files[0]
    if k == 0:
        sys.stderr.write(f'String occurs in no filename of this directory.')
    else:
        sys.stderr.write(f'String occurs in several filenames of this directory.')


def get_bands(product_, src_):

    path = f"{src_}/{product_}/GRANULE"
    r10m = f"{path}/{listdir(path)[0]}/IMG_DATA/R10m"
    r20m = f"{path}/{listdir(path)[0]}/IMG_DATA/R20m"
    scl = find_string_in_directory('SCL', r20m)
    b2 = find_string_in_directory('B02', r10m)
    b3 = find_string_in_directory('B03', r10m)

    return scl, b2, b3, r10m, r20m


def unzip(origin_path, destination_path):

    with zipfile.ZipFile(origin_path, 'r') as zip_ref:
        zip_ref.extractall(destination_path)


def clear(directory_, subdirectories_):
    """Resets the directory."""
    for object_ in listdir(directory_):
        rmtree(f"{directory_}/{object_}")
    for subdirectory_ in subdirectories_:
        makedirs(f"{directory_}/{subdirectory_}")


if __name__ == '__main__':

    pass
