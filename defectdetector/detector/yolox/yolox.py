import cv2
import numpy as np

from defectdetector.utils import singleton


@singleton
class YoloX:
    """Load a pre-training Yolox model from ONNX, and make target prediction for the input image.

    Args:
        modelPath: Path of the model.
        confThreshold: A threshold used to filter boxes by score.
        nmsThreshold: A threshold used in non-maximum suppression.
        backendId: Specific computation backend supported by network.
        targetId: Target identifier of the specific target device used for computations.
    """
    def __init__(self, modelPath, confThreshold=0.35, nmsThreshold=0.5, objThreshold=0.5, backendId=0, targetId=0):
        self.num_classes = 80
        self.net = cv2.dnn.readNetFromONNX(modelPath)
        self.input_size = (640, 640)
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1, 1, 3)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1, 1, 3)
        self.strides = [8, 16, 32]
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        self.objThreshold = objThreshold
        self.backendId = backendId
        self.targetId = targetId
        self.net.setPreferableBackend(self.backendId)
        self.net.setPreferableTarget(self.targetId)

        self.generateAnchors()

    @property
    def name(self):
        """Add attribute of classname.

        Returns:
            name(str): name of class.
        """
        return self.__class__.__name__

    def setBackend(self, backenId):
        """Reset backend identifier for self.net.setPreferableBackend.
        """
        self.backendId = backenId
        self.net.setPreferableBackend(self.backendId)

    def setTarget(self, targetId):
        """Reset target identifier for self.net.setPreferableTarget.
        """
        self.targetId = targetId
        self.net.setPreferableTarget(self.targetId)

    def preprocess(self, img):
        """Pre-processing, changing the input dimension.

        Args:
            img(ndarray): Input image of the model.

        Returns:
            blob(ndarray): Preprocessed image.
        """
        blob = np.transpose(img, (2, 0, 1))
        return blob[np.newaxis, :, :, :]

    def infer(self, srcimg):
        """Infer the prediction of the input image from the model and provide classification.

        Args:
            srcimg(ndarray): Input image of the model.

        Returns:
            predictions(ndarray): Coordinates, classification scores and categories of objectives.
        """
        input_blob = self.preprocess(srcimg)

        self.net.setInput(input_blob)
        outs = self.net.forward(self.net.getUnconnectedOutLayersNames())

        predictions = self.postprocess(outs[0])
        return predictions

    def postprocess(self, outputs):
        """Get the defect category according to the model output.

        Args:
            outputs(ndarray): Output of model.

        Returns:
            candidates(ndarray): All objectives and their categories.
        """
        dets = outputs[0]

        dets[:, :2] = (dets[:, :2] + self.grids) * self.expanded_strides
        dets[:, 2:4] = np.exp(dets[:, 2:4]) * self.expanded_strides

        # get boxes
        boxes = dets[:, :4]
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.

        # get scores and class indices
        scores = dets[:, 4:5] * dets[:, 5:]
        max_scores = np.amax(scores, axis=1)
        max_scores_idx = np.argmax(scores, axis=1)

        # batched-nms, TODO: replace with cv2.dnn.NMSBoxesBatched when OpenCV 4.7.0 is released
        max_coord = boxes_xyxy.max()
        offsets = max_scores_idx * (max_coord + 1)
        boxes_for_nms = boxes_xyxy + offsets[:, None]
        keep = cv2.dnn.NMSBoxes(boxes_for_nms.tolist(), max_scores.tolist(), self.confThreshold, self.nmsThreshold)

        candidates = np.concatenate([boxes_xyxy, max_scores[:, None], max_scores_idx[:, None]], axis=1)
        return candidates[keep]

    def generateAnchors(self):
        """Generate Anchor coordinates at each stride.

        Assign the coordinates at each stride to self.grids.
        Assign the number of coordinates under each step to self.expanded_strides.
        """
        self.grids = []
        self.expanded_strides = []
        hsizes = [self.input_size[0] // stride for stride in self.strides]
        wsizes = [self.input_size[1] // stride for stride in self.strides]

        for hsize, wsize, stride in zip(hsizes, wsizes, self.strides):
            xv, yv = np.meshgrid(np.arange(hsize), np.arange(wsize))
            grid = np.stack((xv, yv), 2).reshape(1, -1, 2)
            self.grids.append(grid)
            shape = grid.shape[:2]
            self.expanded_strides.append(np.full((*shape, 1), stride))

        self.grids = np.concatenate(self.grids, 1)
        self.expanded_strides = np.concatenate(self.expanded_strides, 1)