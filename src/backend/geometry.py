import numpy
from backend.environment import Collimator, Detector, Target


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

    def cutting_collimator_radius(self, diatnce: float) -> float:
        pass

    def xy_plane(self) -> tuple[list[float], list[float]]:
        return (self.coordinates[0], self.coordinates[1])
    
    def xy_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self.first_collimator
        c2 = self.last_collimator

        starting_x = c1.x_position + c1.thickness * 10

        starting_ceil_y = c1.y_position + c1.radius / 2
        starting_floor_y = c1.y_position - c1.radius / 2

        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness * 10, lines)

        reflecting_floor_ys = (c2.y_position - c2.radius / 2) * numpy.ones_like(reflecting_xs)
        reflecting_ceil_ys = (c2.y_position + c2.radius / 2) * numpy.ones_like(reflecting_xs)

        stopping_x = self.detector.x_position

        reflections = []
        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_ceil_y[i]),
                (reflecting_xs[i], reflecting_floor_ys[i]),
                stopping_x
            ))

        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_floor_y[i]),
                (reflecting_xs[i], reflecting_ceil_ys[i]),
                stopping_x
            ))

        return reflections

    def xz_plane(self) -> tuple[list[float], list[float]]:
        return (self.coordinates[0], self.coordinates[2])
    
    def xz_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self.first_collimator
        c2 = self.last_collimator

        starting_x = c1.x_position + c1.thickness * 10

        starting_ceil_z = c1.z_position + c1.radius / 2
        starting_floor_z = c1.z_position - c1.radius / 2

        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness * 10, lines)

        reflecting_floor_zs = (c2.z_position - c2.radius / 2) * numpy.ones_like(reflecting_xs)
        reflecting_ceil_zs = (c2.z_position + c2.radius / 2) * numpy.ones_like(reflecting_xs)

        stopping_x = self.detector.x_position

        reflections = []
        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_ceil_z[i]),
                (reflecting_xs[i], reflecting_floor_zs[i]),
                stopping_x
            ))

        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_floor_z[i]),
                (reflecting_xs[i], reflecting_ceil_zs[i]),
                stopping_x
            ))

        return reflections

    def yz_plane(self) -> tuple[list[float], list[float]]:
        return (self.coordinates[1], self.coordinates[2])

    def yz_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self.first_collimator
        c2 = self.last_collimator

        starting_y = c1.y_position + c1.thickness * 10

        starting_ceil_z = c1.z_position + c1.radius / 2
        starting_floor_z = c1.z_position - c1.radius / 2

        reflecting_ys = numpy.linspace(c2.y_position, c2.y_position + c2.thickness * 10, lines)

        reflecting_floor_zs = (c2.z_position - c2.radius / 2) * numpy.ones_like(reflecting_ys)
        reflecting_ceil_zs = (c2.z_position + c2.radius / 2) * numpy.ones_like(reflecting_ys)

        stopping_y = self.detector.y_position

        reflections = []
        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_y, starting_ceil_z[i]),
                (reflecting_ys[i], reflecting_floor_zs[i]),
                stopping_y
            ))

        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_y, starting_floor_z[i]),
                (reflecting_ys[i], reflecting_ceil_zs[i]),
                stopping_y
            ))

        return reflections

    def __reflections_by(self, 
                         start: tuple[float, float], 
                         reflect: tuple[float, float], 
                         stop_x: float) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        start_x, start_y = start
        reflect_x, reflect_y = reflect

        systematrix = numpy.array([[start_x, 1], [reflect_x, 1]])
        right_hand = numpy.array([start_y, reflect_y])
        coeffs = numpy.linalg.solve(systematrix, right_hand)

        ingoing_xs = numpy.array([start_x, reflect_x])
        outgoing_xs = numpy.array([reflect_x, stop_x])

        ingoing_ys = coeffs[0] * ingoing_xs + coeffs[1]
        outgoing_ys = -coeffs[0] * outgoing_xs - coeffs[1]

        return [(ingoing_xs, ingoing_ys), (outgoing_xs, outgoing_ys)]


if __name__ == '__main__':
    pass
