from imports import *
import numpy as np


def write_string_to_file(string: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(string)
        f.close()


def write_matrix_to_file(matrix: list, path: str) -> None:
    to_write = ""
    for row in matrix:
        for entry in row:
            to_write += '{0: >5}'.format(entry) + "|"
        to_write += '\n'
    with open(path, "w") as f:
        f.write(to_write)
        f.close()


def read_float_from_file(path: str) -> float:
    with open(path, "r") as f:
        return float(f.read())


def read_list_from_file(path: str) -> dict:
    with open(path, "r") as f:
        items = f.read().split(',')
        items[0] = items[0].replace("[", "")
        items[-1] = items[-1].replace("]", "")
        return np.array([float(item) for item in items])


def read_matrix_from_file(path: str) -> list:
    matrix = []
    with open(path, "r") as f:
        for line in f.readlines():
            entries = line.split('|')
            matrix.append([int(entry.strip())
                          for entry in entries if entry.strip() != ""])
    return np.matrix(matrix)
