
"""
此包用于定义缺陷检测算法
"""

from .yolox.inference import YoloxDetector
from .base import Detector

__all__ = [
    'Detector', 'YoloxDetector'
]
