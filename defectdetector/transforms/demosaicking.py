import cv2 as cv

from typing import Dict
from .base import BaseTransform


class Demosaic(BaseTransform):

    def __init__(self):
        super(Demosaic, self).__init__()

    def __call__(self, img_info: Dict, interpolation=True):
        img = img_info['img']

        height, width, channel = img.shape

        _polar_angle = [i_0, i_45, i_90, i_135] = \
            img[0::2, 0::2, :], img[0::2, 1::2, :], img[1::2, 0::2, :], img[1::2, 1::2, :]

        if interpolation:
            _polar_angle = [i_0, i_45, i_90, i_135] = \
                [cv.resize(_img, (width, height), interpolation=cv.INTER_NEAREST) for _img in _polar_angle]

        s0 = (i_0 + i_90 + i_45 + i_135) * 2
        s1 = i_0 - i_90
        s2 = i_45 - i_135

        img_info['polar_angle'] = _polar_angle
        img_info['stokes'] = [s0, s1, s2]

        return img_info
