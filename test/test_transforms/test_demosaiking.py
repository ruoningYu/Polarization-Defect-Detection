import cv2 as cv
import time

from defectdetector.transforms.demosaicking import Demosaic
from defectdetector.transforms.utils import pixel_normalization


def test_demosaicking():
    save = True
    img = cv.imread("../data/test_raw.bmp")

    img_info = dict(img=img)

    demosaic = Demosaic()
    start_time = time.time()
    res = demosaic(img_info)
    end_time = time.time()

    cost = end_time - start_time

    stokes = res['stokes']
    polar_angles = res['polar_angle']

    assert len(stokes) == 3 and len(polar_angles) == 4
    assert stokes[0].shape[0] == img.shape[0] and polar_angles[0].shape[0] == img.shape[0]

    i0 = polar_angles[0]
    print(f'i0: {i0.shape} img: {img.shape} \n')
    print(f'cost time: {cost}')

    if save:
        cv.imwrite("i0.jpg", i0)
        cv.imwrite("i45.jpg", polar_angles[1])
        cv.imwrite("i90.jpg", polar_angles[2])
        cv.imwrite("i135.jpg", polar_angles[3])
