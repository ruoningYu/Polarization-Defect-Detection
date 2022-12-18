"""
此包用于定义缺陷检测算法
"""

from .base import Detector
from .yolox.inference import YoloxDetector

__all__ = [
    'Detector', 'YoloxDetector'
]
