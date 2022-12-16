"""
此文件用于图像预处理
"""
from .base import BaseTransform
from .resize import Resize, ConvertColorspace


class Transforms:
    METHOD = [
        Resize, ConvertColorspace
    ]


__all__ = [
    'BaseTransform', 'Transforms'
]
