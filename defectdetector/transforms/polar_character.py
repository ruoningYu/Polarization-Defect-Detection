import cv2 as cv
import numpy as np

from typing import List, Dict
from numba import njit
from .base import BaseTransform
from .utils import pixel_normalization


@njit()
def aolp(stokes):
    aolp = np.mod(0.5 * np.arctan(stokes[2] / stokes[1]) * 180 / np.pi, 180)
    return aolp


@njit()
def dolp(stokes):
    return np.sqrt(np.power(stokes[1], 2) + np.power(stokes[2], 2)) / stokes[0]


@njit()
def l1(stokes):
    return stokes[1] / stokes[0]


@njit()
def l2(stokes):
    return stokes[2] / stokes[0]


@njit()
def sp(stokes):
    return np.power(np.power(stokes[1], 2) + np.power(stokes[2], 2), 0.5)


@njit()
def snp(stokes):
    return stokes[0] - sp(stokes[1], stokes[2])


class PolarCharacter(BaseTransform):

    def __init__(self, characters: List = []):
        super(PolarCharacter, self).__init__()
        self.characters = characters

    def __call__(self, img_info: Dict):
        _polar_angle = img_info['polar_angle']
        stokes = img_info['stokes']

        img_info['aolp'] = aolp(stokes)
        img_info['dolp'] = dolp(stokes)
        # img_info['l1'] = dolp(stokes)
        # img_info['l2'] = dolp(stokes)

        return img_info
