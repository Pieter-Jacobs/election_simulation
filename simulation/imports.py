import os
import hydra
from omegaconf import DictConfig, OmegaConf
from scipy import spatial
from numba import njit
from sklearn.decomposition import PCA
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt