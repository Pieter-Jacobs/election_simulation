from imports import *

@njit
def cosine_similarity(v1, v2):
    """Compute the cosine similarity between vectors v1 and v2"""
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y

    return sumxy/((sumxx**0.5)*(sumyy**0.5))

