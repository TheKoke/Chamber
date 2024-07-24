import numpy
from backend.environment import Environment, Collimator, Detector, Target


class Geometry:
    def __init__(self, first: Collimator, last: Collimator, trgt: Target, det: Detector) -> None:
        self.__first_collimator = first
        self.__last_collimator = last
        self.__target = trgt
        self.__detector = det
        self._environments: list[Environment] = [first, last, trgt, det]

    @property
    def first_collimator(self) -> Collimator:
        return self.__first_collimator
    
    @property
    def last_collimator(self) -> Collimator:
        return self.__last_collimator
    
    @property
    def target(self) -> Target:
        return self.__target
    
    @property
    def detector(self) -> Detector:
        return self.__detector

    @staticmethod
    def projection_formula(d1: float, h1: float, d2: float) -> float:
        return h1 * (d2 / d1)
    
    def cutting_collimator_radius(self, distance: float) -> float:
        pass

    def xy_optics(self) -> list[list[float]]:
        h1 = self.__first_collimator.radius
        h2 = self.__last_collimator.radius
        
        crossing_h = self.__last_collimator.x_position - h1 * self.__last_collimator.x_position / (h1 + h2)
        d1 = self.__last_collimator.x_position - crossing_h
        d2_target = self.__target.x_position - crossing_h
        d2_detector = self.__detector.x_position - crossing_h

        on_target = Geometry.projection_formula(d1, h1, d2_target)
        on_detector = Geometry.projection_formula(d1, h1, d2_detector)

        xs = []
        for i in range(len(self._environments)):
            xs.append(self._environments[i].x_position)
            xs.append(self._environments[i].x_position)

        ys = [
            self.__first_collimator.radius / 2, -self.__first_collimator.radius / 2,
            self.__last_collimator.radius / 2, -self.__last_collimator.radius / 2,
        ]
    
    def xy_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self.__first_collimator
        c2 = self.__last_collimator

        starting_x = c1.x_position

        starting_ceil_y = c1.y_position + c1.radius / 2
        starting_floor_y = c1.y_position - c1.radius / 2

        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness * 10, lines)

        reflecting_floor_ys = (c2.y_position - c2.radius / 2) * numpy.ones_like(reflecting_xs)
        reflecting_ceil_ys = (c2.y_position + c2.radius / 2) * numpy.ones_like(reflecting_xs)

        stopping_x = self.__detector.x_position

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
        pass
    
    def xz_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self.__first_collimator
        c2 = self.__last_collimator

        starting_x = c1.x_position

        starting_ceil_z = c1.z_position + c1.radius / 2
        starting_floor_z = c1.z_position - c1.radius / 2

        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness * 10, lines)

        reflecting_floor_zs = (c2.z_position - c2.radius / 2) * numpy.ones_like(reflecting_xs)
        reflecting_ceil_zs = (c2.z_position + c2.radius / 2) * numpy.ones_like(reflecting_xs)

        stopping_x = self.__detector.x_position

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
        pass

    def yz_reflections(self) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self.__first_collimator
        c2 = self.__last_collimator

        starting_y = c1.y_position

        starting_ceil_z = c1.z_position + c1.radius / 2
        starting_floor_z = c1.z_position - c1.radius / 2

        reflecting_ys = numpy.linspace(c2.y_position, c2.y_position + c2.thickness * 10, lines)

        reflecting_floor_zs = (c2.z_position - c2.radius / 2) * numpy.ones_like(reflecting_ys)
        reflecting_ceil_zs = (c2.z_position + c2.radius / 2) * numpy.ones_like(reflecting_ys)

        stopping_y = self.__detector.y_position

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
