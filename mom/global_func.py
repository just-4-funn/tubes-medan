import math
import numpy as np


def power2(x):
    return x * x


def sqrt(x):
    return math.sqrt(x)


def inv(m):
    a, b = m.shape
    if a != b:
        raise ValueError("Only square matrices are invertible.")

    i = np.eye(a, a)
    return np.linalg.lstsq(m, i, rcond=-1)[0]