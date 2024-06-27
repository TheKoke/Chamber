import numpy
from environment import Collimator, Detector, Target


class Geometry:
    def __init__(self, first: Collimator, last: Collimator, trgt: Target, det: Detector) -> None:
        self.first_collimator = first
        self.last_collimator = last
        self.target = trgt
        self.detector = det

        self.dots = self.build_coordinates()

    def build_coordinates(self) -> None:
        pass


if __name__ == '__main__':
    pass
