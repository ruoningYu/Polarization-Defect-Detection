"""
此文件用于图像预处理
"""
from .base import BaseTransform
from .resize import Resize, ConvertColorspace
from .demosaicking import Demosaic
from .polar_character import PolarCharacter


class Transforms:
    METHOD = [
        Resize, ConvertColorspace, Demosaic, PolarCharacter
    ]


__all__ = [
    'BaseTransform', 'Transforms'
]
