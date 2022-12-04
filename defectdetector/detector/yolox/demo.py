import numpy as np
import cv2
import argparse

from yolox import YoloX


def str2bool(v):
    if v.lower() in ['on', 'yes', 'true', 'y', 't']:
        return True
    elif v.lower() in ['off', 'no', 'false', 'n', 'f']:
        return False
    else:
        raise NotImplementedError


model = "../model/yolox_s.onnx"
confidence = 0.5
nms = 0.5
obj = 0.5

backends = [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_BACKEND_CUDA]
targets = [cv2.dnn.DNN_TARGET_CPU, cv2.dnn.DNN_TARGET_CUDA, cv2.dnn.DNN_TARGET_CUDA_FP16]
help_msg_backends = "Choose one of the computation backends: {:d}: OpenCV implementation (default); {:d}: CUDA"
help_msg_targets = "Chose one of the target computation devices: {:d}: CPU (default); {:d}: CUDA; {:d}: CUDA fp16"

try:
    backends += [cv2.dnn.DNN_BACKEND_TIMVX]
    targets += [cv2.dnn.DNN_TARGET_NPU]
    help_msg_backends += "; {:d}: TIMVX"
    help_msg_targets += "; {:d}: NPU"
except:
    print(
        'This version of OpenCV does not support TIM-VX and NPU. Visit https://github.com/opencv/opencv/wiki/TIM-VX-Backend-For-Running-OpenCV-On-NPU for more information.')


classes = ("right_port",
           "left_port",
           "right_port_back",
           "left_port_back",
           "poor_clean",
           "scratch",
           "bruised")


def letterbox(srcimg, target_size=(640, 640)):
    padded_img = np.ones((target_size[0], target_size[1], 3)) * 114.0
    ratio = min(target_size[0] / srcimg.shape[0], target_size[1] / srcimg.shape[1])
    resized_img = cv2.resize(
        srcimg, (int(srcimg.shape[1] * ratio), int(srcimg.shape[0] * ratio)), interpolation=cv2.INTER_LINEAR
    ).astype(np.float32)
    padded_img[: int(srcimg.shape[0] * ratio), : int(srcimg.shape[1] * ratio)] = resized_img

    return padded_img, ratio


def unletterbox(bbox, letterbox_scale):
    return bbox / letterbox_scale


def vis(dets, srcimg, letterbox_scale, fps=None):
    res_img = srcimg.copy()

    if fps is not None:
        fps_label = "FPS: %.2f" % fps
        cv2.putText(res_img, fps_label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    for det in dets:
        box = unletterbox(det[:4], letterbox_scale).astype(np.int32)
        score = det[-2]
        cls_id = int(det[-1])

        x0, y0, x1, y1 = box

        text = '{}:{:.1f}%'.format(classes[cls_id], score * 100)
        font = cv2.FONT_HERSHEY_SIMPLEX
        txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
        cv2.rectangle(res_img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2.rectangle(res_img, (x0, y0 + 1), (x0 + txt_size[0] + 1, y0 + int(1.5 * txt_size[1])), (255, 255, 255), -1)
        cv2.putText(res_img, text, (x0, y0 + txt_size[1]), font, 0.4, (0, 0, 0), thickness=1)

    return res_img


def inference(input):
    model_net = YoloX(modelPath=model,
                      confThreshold=confidence,
                      nmsThreshold=nms,
                      objThreshold=obj,
                      backendId=backends[0],
                      targetId=targets[0])

    tm = cv2.TickMeter()
    tm.reset()

    input_blob = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
    input_blob, letterbox_scale = letterbox(input_blob)

    # Inference
    tm.start()
    preds = model_net.infer(input_blob)
    tm.stop()
    print("Inference time: {:.2f} ms".format(tm.getTimeMilli()))

    img = vis(preds, input, letterbox_scale)

    cv2.namedWindow("Test", (612, 512))
    cv2.imshow("Test", img)
    cv2.waitKey(0)

    return img
