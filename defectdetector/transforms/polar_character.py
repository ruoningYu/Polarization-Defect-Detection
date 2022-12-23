import cv2 as cv
import numpy as np

from typing import List, Dict
from numba import njit
from .base import BaseTransform
from .utils import pixel_normalization


@njit()
def aolp(stokes):
    """Compute AoLP

    Args:
        stokes: Stokes parameters

    Returns:
        aolp (ndarray): AoLp
    """
    return np.mod(0.5 * np.arctan(stokes[2] / stokes[1]) * 180 / np.pi, 180)


@njit()
def dolp(stokes):
    """Compute DoLP

    Args:
        stokes: Stokes parameters

    Returns:
        aolp (ndarray): DoLp
    """
    return np.sqrt(np.power(stokes[1], 2) + np.power(stokes[2], 2)) / stokes[0]


@njit()
def l1(stokes):
    """Compute L1

    Args:
        stokes: Stokes parameters

    Returns:
        L1 (ndarray): L1
    """
    return stokes[1] / stokes[0]


@njit()
def l2(stokes):
    """Compute L2

    Args:
        stokes: Stokes parameters

    Returns:
        L2 (ndarray): L2
    """
    return stokes[2] / stokes[0]


@njit()
def sp(stokes):
    """Compute sp

    Args:
        stokes: Stokes parameters

    Returns:
        sp (ndarray): sp
    """
    return np.power(np.power(stokes[1], 2) + np.power(stokes[2], 2), 0.5)


@njit()
def snp(stokes):
    """Compute snp

    Args:
        stokes: Stokes parameters

    Returns:
        snp (ndarray): snp
    """
    return stokes[0] - sp(stokes[1], stokes[2])


class PolarCharacter(BaseTransform):
    """Compute polarization characterization image

    Args:
        characters (List): Parameters to be calculated
    """
    def __init__(self, characters: List = []):
        super(PolarCharacter, self).__init__()
        self.characters = characters

    def __call__(self, img_info: Dict):
        """

        Args:
            img_info (Dict): Image info

        Returns:
            img_info (Dict): Image info
        """
        _polar_angle = img_info['polar_angle']
        stokes = img_info['stokes']

        img_info['aolp'] = pixel_normalization(aolp(stokes))

        img_info['dolp'] = dolp(stokes)
        # img_info['l1'] = dolp(stokes)
        # img_info['l2'] = dolp(stokes)

        return img_info
