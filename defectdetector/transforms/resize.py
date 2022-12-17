import cv2 as cv

from typing import Dict
from .base import BaseTransform


class Resize(BaseTransform):

    def __init__(self):
        super(Resize, self).__init__()

    def __call__(self, img_info: Dict):
        img_info['img'] = cv.resize(img_info['img'], (612, 512))
        return img_info


class ConvertColorspace(BaseTransform):

    def __init__(self):
        super(ConvertColorspace, self).__init__()

    def __call__(self,
                 img_info: Dict,
                 convert_mode='COLOR_GRAY2RGB'):
        img_info['img'] = cv.cvtColor(img_info['img'], getattr(cv, convert_mode))
        return img_info
