import numpy
from environment import Collimator, Detector, Target


class Geometry:
    def __init__(self, first: Collimator, last: Collimator, trgt: Target, det: Detector) -> None:
        self.first_collimator = first
        self.last_collimator = last
        self.target = trgt
        self.detector = det

        self.distances = self.build_distances()
        self.heights = self.build_heights()
        self.widths = self.build_widths()
        self.coordinates = self.build_coordinates()

    def build_distances(self) -> list[float]:
        first_x = self.first_collimator.x_position
        second_x = self.last_collimator.x_position
        third_x = self.target.x_position
        fourth_x = self.detector.x_position

        distances = [0]
        x_positions = [first_x, second_x, third_x, fourth_x]
        for i in range(len(x_positions) - 1):
            distances.append(x_positions[i + 1] - x_positions[i])

        return distances

    def build_heights(self) -> list[float]:
        h1 = self.first_collimator.radius
        h2 = self.last_collimator.radius
        t1 = self.first_collimator.thickness
        t2 = self.last_collimator.thickness

        crossing_h = self.distances[1] - h1 * self.distances[1] / (h1 + h2)

        h3 = h2 * (crossing_h + self.distances[2] - t1) / crossing_h
        h4 = h2 * (crossing_h + self.distances[2] + self.distances[3] + t2) / crossing_h

        return [h1, h2, h3, h4]
    
    def build_widths(self) -> list[float]:
        w1 = self.first_collimator.radius
        w2 = self.last_collimator.radius
        t1 = self.first_collimator.thickness
        t2 = self.last_collimator.thickness

        crossing_w = self.distances[1] - w1 * self.distances[1] / (w1 + w2)

        w3 = w2 * (crossing_w + self.distances[2] - t1) / crossing_w
        w4 = w2 * (crossing_w + self.distances[2] + self.distances[3] + t2) / crossing_w

        return [w1, w2, w3, w4]

    def build_coordinates(self) -> tuple[list[float], list[float], list[float]]:
        dots = ([], [], [])
        for i in range(len(self.distances)): # x-coordinates
            dots[0].append(sum(self.distances[:i + 1]))
            dots[0].append(sum(self.distances[:i + 1]))

        for i in range(len(self.heights)): # y-coordinates
            dots[1].append(-self.heights[i] / 2)
            dots[1].append(self.heights[i] / 2)

        for i in range(len(self.widths)): # z-coordinates
            dots[2].append(-self.widths[i] / 2)
            dots[2].append(self.widths[i] / 2)

        return dots
    
    def refresh(self) -> None:
        self.distances = self.build_distances()
        self.heights = self.build_heights()
        self.widths = self.build_widths()
        self.coordinates = self.build_coordinates()

    def xy_plane(self) -> tuple[list[float], list[float]]:
        return (self.coordinates[0], self.coordinates[1])
    
    def xy_reflections(self) -> list[numpy.ndarray]:
        pass

    def xz_plane(self) -> tuple[list[float], list[float]]:
        return (self.coordinates[0], self.coordinates[2])
    
    def xz_reflections(self) -> list[numpy.ndarray]:
        pass

    def yz_plane(self) -> tuple[list[float], list[float]]:
        return (self.coordinates[1], self.coordinates[2])

    def yz_reflections(self) -> list[numpy.ndarray]:
        pass


if __name__ == '__main__':
    pass
