import hydra
import os
from numba import njit
from numpy.lib.function_base import average
from omegaconf import DictConfig, OmegaConf