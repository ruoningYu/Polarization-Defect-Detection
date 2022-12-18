import cv2 as cv
import time

from defectdetector.transforms.demosaicking import Demosaic
from defectdetector.transforms.polar_character import PolarCharacter
from defectdetector.transforms.utils import pixel_normalization


def test_polar():
    save = True
    img = cv.imread("../data/test_raw.bmp")

    img_info = dict(img=img)

    start_time = time.time()
    demosaic = Demosaic()
    res_demosaic = demosaic(img_info)

    polar_characters = PolarCharacter()
    res = polar_characters(res_demosaic)

    end_time = time.time()
    cost = end_time - start_time

    aolp = res['aolp']

    dolp = res['dolp']

    assert aolp.shape == img.shape

    aolp = pixel_normalization(aolp)
    dolp = pixel_normalization(dolp)

    print(f'cost time: {cost}')
    #
    if save:
        cv.imwrite("aolp.jpg", aolp)
        cv.imwrite("dolp.jpg", dolp)

