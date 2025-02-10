import numpy
from backend.environment import Environment, Collimator, Detector, Target


class Geometry:
    def __init__(self, collimators: list[Collimator], target: Target, detector: Detector) -> None:
        self._collimators = collimators
        self._first_collimator = collimators[0]
        self._last_collimator = collimators[-1]
        self._target = target
        self._detector = detector

        self._pivots: list[Environment] = [collimators[0], collimators[-1], target, detector]
        self._environments: list[Environment] = [*collimators, target, detector]

    @property
    def collimators(self) -> list[Collimator]:
        return self._collimators.copy()

    @property
    def first_collimator(self) -> Collimator:
        return self._first_collimator
    
    @property
    def last_collimator(self) -> Collimator:
        return self._last_collimator
    
    @property
    def target(self) -> Target:
        return self._target
    
    @property
    def detector(self) -> Detector:
        return self._detector

    @staticmethod
    def projection_formula(d1: float, h1: float, d2: float) -> float:
        return h1 * (d2 / d1)
    
    def spot_at_distance(self, distance: float) -> float:
        h1 = self._first_collimator.radius
        h2 = self._last_collimator.radius
        
        crossing_h = self._last_collimator.x_position - h1 * self._last_collimator.x_position / (h1 + h2)
        d1 = self._last_collimator.x_position - crossing_h

        return Geometry.projection_formula(d1, h2, distance - crossing_h)
    
    def spot_on_target(self) -> float:
        return self.spot_at_distance(self._target.x_position)

    def spot_on_detector(self) -> float:
        return self.spot_at_distance(self._detector.x_position)
    
    def angle_resolution(self) -> float:
        angle_scale = 360 / (2 * numpy.pi * (self._detector.x_position - self._target.x_position))
        return angle_scale * self.spot_on_detector() / 2

    def xy_optics(self) -> list[list[float]]:
        xs = []
        for i in range(len(self._pivots)):
            xs.append(self._pivots[i].x_position)
            xs.append(self._pivots[i].x_position)

        ys = [
            self._first_collimator.radius / 2 + self._first_collimator.y_position,
            -self._first_collimator.radius / 2 + self._first_collimator.y_position,
            self._last_collimator.radius / 2 + self._last_collimator.y_position, 
            -self._last_collimator.radius / 2 + self._last_collimator.y_position,
        ]

        first_coeffs = numpy.linalg.solve(numpy.array([[xs[0], 1], [xs[2], 1]]), numpy.array([ys[0], ys[3]]))
        second_coeffs = numpy.linalg.solve(numpy.array([[xs[1], 1], [xs[3], 1]]), numpy.array([ys[1], ys[2]]))

        for i in range(2, len(self._pivots)):
            ys.append(second_coeffs[0] * self._pivots[i].x_position + second_coeffs[1])
            ys.append(first_coeffs[0] * self._pivots[i].x_position + first_coeffs[1])

        return [xs, ys]
    
    def xy_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self._first_collimator
        c2 = self._last_collimator

        starting_x = c1.x_position

        starting_ceil_y = c1.y_position + c1.radius / 2
        starting_floor_y = c1.y_position - c1.radius / 2

        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness * 10, lines)

        reflecting_floor_ys = (c2.y_position - c2.radius / 2) * numpy.ones_like(reflecting_xs)
        reflecting_ceil_ys = (c2.y_position + c2.radius / 2) * numpy.ones_like(reflecting_xs)

        stopping_x = self._detector.x_position

        reflections = []
        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_ceil_y),
                (reflecting_xs[i], reflecting_floor_ys[i]),
                stopping_x
            ))

        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_floor_y),
                (reflecting_xs[i], reflecting_ceil_ys[i]),
                stopping_x
            ))

        return reflections
    
    def xz_optics(self) -> list[list[float]]:
        xs = []
        for i in range(len(self._pivots)):
            xs.append(self._pivots[i].x_position)
            xs.append(self._pivots[i].x_position)

        zs = [
            self._first_collimator.radius / 2 + self._first_collimator.z_position,
            -self._first_collimator.radius / 2 + self._first_collimator.z_position,
            self._last_collimator.radius / 2 + self._last_collimator.z_position, 
            -self._last_collimator.radius / 2 + self._last_collimator.z_position,
        ]

        first_coeffs = numpy.linalg.solve(numpy.array([[xs[0], 1], [xs[2], 1]]), numpy.array([zs[0], zs[3]]))
        second_coeffs = numpy.linalg.solve(numpy.array([[xs[1], 1], [xs[3], 1]]), numpy.array([zs[1], zs[2]]))

        for i in range(2, len(self._pivots)):
            zs.append(second_coeffs[0] * self._pivots[i].x_position + second_coeffs[1])
            zs.append(first_coeffs[0] * self._pivots[i].x_position + first_coeffs[1])

        return [xs, zs]
    
    def xz_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self._first_collimator
        c2 = self._last_collimator

        starting_x = c1.x_position

        starting_ceil_z = c1.z_position + c1.radius / 2
        starting_floor_z = c1.z_position - c1.radius / 2

        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness * 10, lines)

        reflecting_floor_zs = (c2.z_position - c2.radius / 2) * numpy.ones_like(reflecting_xs)
        reflecting_ceil_zs = (c2.z_position + c2.radius / 2) * numpy.ones_like(reflecting_xs)

        stopping_x = self._detector.x_position

        reflections = []
        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_ceil_z),
                (reflecting_xs[i], reflecting_floor_zs[i]),
                stopping_x
            ))

        for i in range(lines):
            reflections.extend(self.__reflections_by(
                (starting_x, starting_floor_z),
                (reflecting_xs[i], reflecting_ceil_zs[i]),
                stopping_x
            ))

        return reflections
    
    def yz_optics(self) -> None:
        ys = []
        for i in range(len(self._pivots)):
            ys.append(self._pivots[i].y_position)
            ys.append(self._pivots[i].y_position)

        zs = [
            self._first_collimator.radius / 2 + self._first_collimator.z_position,
            -self._first_collimator.radius / 2 + self._first_collimator.z_position,
            self._last_collimator.radius / 2 + self._last_collimator.z_position, 
            -self._last_collimator.radius / 2 + self._last_collimator.z_position,
        ]

        first_coeffs = numpy.linalg.solve(numpy.array([[ys[0], 1], [ys[2], 1]]), numpy.array([zs[0], zs[3]]))
        second_coeffs = numpy.linalg.solve(numpy.array([[ys[1], 1], [ys[3], 1]]), numpy.array([zs[1], zs[2]]))

        for i in range(2, len(self._pivots)):
            zs.append(second_coeffs[0] * self._pivots[i].y_position + second_coeffs[1])
            zs.append(first_coeffs[0] * self._pivots[i].y_position + first_coeffs[1])

        return [ys, zs]

    def yz_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self._first_collimator
        c2 = self._last_collimator

        starting_y = c1.y_position

        starting_ceil_z = c1.z_position + c1.radius / 2
        starting_floor_z = c1.z_position - c1.radius / 2

        reflecting_ys = numpy.linspace(c2.y_position, c2.y_position + c2.thickness * 10, lines)

        reflecting_floor_zs = (c2.z_position - c2.radius / 2) * numpy.ones_like(reflecting_ys)
        reflecting_ceil_zs = (c2.z_position + c2.radius / 2) * numpy.ones_like(reflecting_ys)

        stopping_y = self._detector.y_position

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
        outgoing_ys = -coeffs[0] * outgoing_xs + coeffs[0] * reflect_x + reflect_y

        return [(ingoing_xs, ingoing_ys), (outgoing_xs, outgoing_ys)]


if __name__ == '__main__':
    pass
