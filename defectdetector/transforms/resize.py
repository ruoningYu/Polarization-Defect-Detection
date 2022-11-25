
import cv2 as cv
from .base import BaseTransform


class Resize(BaseTransform):

    def __init__(self):
        super(Resize, self).__init__()

    def __call__(self, img):
        res = cv.resize(img, (612, 512))
        return res


class ConvertColorspace(BaseTransform):

    def __init__(self):
        super(ConvertColorspace, self).__init__()

    def __call__(self, 
                 img, 
                 convert_mode='COLOR_GRAY2RGB'):
        res = cv.cvtColor(img, getattr(cv, convert_mode))
        return res

