import os
import hydra
from omegaconf import DictConfig, OmegaConf
from scipy import spatial
from numba import njit