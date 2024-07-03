import numpy
from environment import Collimator, Detector, Target


class Geometry:
    def __init__(self, first: Collimator, last: Collimator, trgt: Target, det: Detector) -> None:
        self.first_collimator = first
        self.last_collimator = last
        self.target = trgt
        self.detector = det

        self.distances = self.build_distances()
        self.dots = self.build_coordinates()

    def build_distances(self) -> list[float]:
        first_x = self.first_collimator.x_position
        second_x = self.last_collimator.x_position
        third_x = self.target.x_position
        fourth_x = self.detector.x_position

        self.dots = []
        x_positions = [first_x, second_x, third_x, fourth_x]
        for i in range(len(x_positions) - 1):
            self.dots.append(x_positions[i + 1] - x_positions[i])

    def build_coordinates(self) -> None:
        pass


if __name__ == '__main__':
    pass
