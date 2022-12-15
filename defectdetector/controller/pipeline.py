
from defectdetector.transforms import Transforms


class Pipeline:
    """Manager of image processing or defect detection methods.

    Args:
        log (Logger): Record processing process or runtime error
        pipeline (list): List containing various processing methods
    """
    def __init__(self,
                 log,
                 pipeline=None,
                 ):
        self.log = log
        self.pipeline = self.setup(pipeline)

    def setup(self, pipeline):
        """Initialize the process in the pipeline

        Args:
            pipeline (list):  List containing various image processing methods
            or detection methods

        Returns:
            pipeline (list):  List containing various image processing methods
            or detection methods
        """
        _pipeline = []

        for i, p in enumerate(Transforms.METHOD):
            if p in pipeline:
                _pipeline.append(Transforms.METHOD[i])
        return _pipeline

    def add(self, processor):
        """Add a process to the pipeline

        Args:
            processor (): Image processing method or detection method
        """
        self.pipeline.append(processor)

    def remove(self, name):
        """Remove the processor from the pipeline

        Args:
            name (str): The name of the processor to be removed

        Returns:
            bool : Indicates whether the removal is successful
        """
        for i, p in enumerate(self.pipeline):
            if p.__class__.__name__ == name:
                del self.pipeline[i]
                return True
        return False

    def run(self, frame):
        """Run the pipeline to process the target image

        Args:
            frame (ndarray): Images to be processed

        Returns:
            frame (ndarray): Image that completes all processing procedures
        """
        for p in self.pipeline:
           frame = p()(frame)
        return frame