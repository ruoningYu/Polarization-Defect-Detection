import cv2
import numpy as np

from typing import Dict
from PIL import Image, ImageDraw, ImageFont
from defectdetector.utils import singleton


from .yolox import YoloX
from ..base import Detector


class YoloxDetector(Detector):
    """Get the detection results of Yolox and display the defect classification and score.

    Attributes:
        model (str): Path of the model.
        confidence (float): A threshold used to filter boxes by score.
        nms (float): A threshold used in non-maximum suppression.
        classes (tuple): All categories of defects.
        backends (list): Specific computation backend supported by network.
        targets (list): Target identifier of the specific target device used for computations.
        model_net (yolox.YoloX): An instance of the Yolox class.
    """
    def __init__(self):
        super(YoloxDetector, self).__init__()

        self.model = "defectdetector/detector/model/yolox_s.onnx"
        self.confidence = 0.75
        self.nms = 0.5
        self.obj = 0.5

        self.classes = ("right_port",
                        "left_port",
                        "right_port_back",
                        "left_port_back",
                        "poor_clean",
                        "scratch",
                        "bruised")

        self.backends = [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_BACKEND_CUDA]
        self.targets = [cv2.dnn.DNN_TARGET_CPU, cv2.dnn.DNN_TARGET_CUDA, cv2.dnn.DNN_TARGET_CUDA_FP16]

        self.model_net = YoloX(modelPath=self.model,
                               confThreshold=self.confidence,
                               nmsThreshold=self.nms,
                               objThreshold=self.obj,
                               backendId=self.backends[0],
                               targetId=self.targets[0])

    @staticmethod
    def letterbox(srcimg, target_size=(640, 640)):
        """Scale the image and get the scaling ratio.

        Args:
            srcimg (ndarray): Input image.
            target_size (tuple): Input Size.

        Returns:
            padded_img (ndarray): Scaled image.
            ratio (float): Scaling ratio.
        """
        padded_img = np.ones((target_size[0], target_size[1], 3)) * 114.0
        ratio = min(target_size[0] / srcimg.shape[0], target_size[1] / srcimg.shape[1])
        resized_img = cv2.resize(
            srcimg, (int(srcimg.shape[1] * ratio), int(srcimg.shape[0] * ratio)), interpolation=cv2.INTER_LINEAR
        ).astype(np.float32)
        padded_img[: int(srcimg.shape[0] * ratio), : int(srcimg.shape[1] * ratio)] = resized_img

        return padded_img, ratio

    @staticmethod
    def unletterbox(bbox, letterbox_scale):
        return bbox / letterbox_scale

    def vis(self, dets, srcimg, letterbox_scale):
        """Visualize all defect information.

        Args:
            dets (ndarray): Output of the Yolox model.
            srcimg (ndarray): Input image.
            letterbox_scale (float): Scaling ratio.

        Returns:
            res_img (ndarray): Image containing defect information.
        """
        res_img = srcimg.copy()

        class_type = []

        for det in dets:
            box = self.unletterbox(det[:4], letterbox_scale).astype(np.int32)
            score = det[-2]

            if score < 0.5:
                continue

            cls_id = int(det[-1])

            x0, y0, x1, y1 = box
            class_name = self.classes[cls_id]

            if class_name not in class_type:
                class_type.append(class_name)

            text = '{}:{:.1f}%'.format(class_name, score * 100)

            font = cv2.FONT_HERSHEY_SIMPLEX
            txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
            cv2.rectangle(res_img, (x0, y0), (x1, y1), (0, 255, 0), 2)
            cv2.rectangle(res_img, (x0, y0 + 1), (x0 + txt_size[0] + 1, y0 + int(1.5 * txt_size[1])), (255, 255, 255),
                          -1)
            cv2.putText(res_img, text, (x0, y0 + txt_size[1]), font, 0.4, (0, 0, 0), thickness=1)

        if "right_port" not in class_type:
            res_text = "右侧端子缺失！"
        elif "left_port" not in class_type:
            res_text = "左侧端子缺失！"
        else:
            res_text = "端子完整！"

        res_img = paint_chinese_opencv(res_img, res_text, 10, 25)

        return res_img

    def detect(self, frame_info: Dict):
        """Used to create a callable type to visualize all defect information.

        Args:
            frame_info (ndarray): Input image Info.

        Returns:
            img (ndarray): Output image with defect information.
        """
        input_blob, letterbox_scale = self.letterbox(frame_info['img'])
        preds = self.model_net.infer(input_blob)

        frame_info['msg'] = dict(
            preds=preds, letterbox_scale=letterbox_scale
        )
        return frame_info


def paint_chinese_opencv(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    """Display and add Chinese characters on the image

    Args:
        img (ndarray):  Images that need to add Chinese characters.
        text (str): Text to be added.
        left (int): The coordinates of the text, left.
        top (int): The coordinates of the text, top.
        textColor (tuple): Color of text.
        textSize (int): Font size of text.

    Returns:
        ndarray: Image with text added
    """
    if isinstance(img, np.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(img)
    font_style = ImageFont.truetype("defectdetector/utils/heiti.ttc",
                                    textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=font_style)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)