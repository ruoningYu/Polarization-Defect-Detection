import numpy as np


def pixel_normalization(img):
    """Standardize the image

    Args:
        img (ndarray): Image to be processed

    Returns:
        img (ndarray): Processed image
    """
    max_img = np.ones(img.shape) * np.nanmax(img)
    min_img = np.ones(img.shape) * np.nanmin(img)
    _img = max_img - min_img
    res = ((img - min_img) / _img) * 255
    res[np.isnan(res)] = 0
    return np.array(res, dtype=np.int32)

