import numpy
from backend.environment import *


class Optics:
    def __init__(self, tube: Tube) -> None:
        self.__tube = tube

    @property
    def tube(self) -> Tube:
        return self.__tube
    
    def get_lines(self, stop: float, plane: str = 'xy') -> list[list[numpy.ndarray]]:
        coeffs = self.get_coefficients(plane)

        x1, x2 = self.__tube.x_positions()
        x1 += self.__tube.first_collimator.thickness
        x2 += self.__tube.second_collimator.thickness
        xs = numpy.array([x1, x2, stop])
        
        lines = []
        for i in range(len(coeffs)):
            lines.append([xs, coeffs[i][0] * xs + coeffs[i][1]])

        return lines

    def get_coefficients(self, plane: str) -> tuple[numpy.ndarray, numpy.ndarray]:
        diam1, diam2 = self.__tube.first_collimator.diameter, self.__tube.second_collimator.diameter
        x1, x2 = self.__tube.x_positions()

        if plane == 'xy':
            y1, y2 = self.__tube.first_collimator.y_position, self.__tube.second_collimator.y_position

        if plane == 'xz':
            y1, y2 = self.__tube.first_collimator.z_position, self.__tube.second_collimator.z_position

        x1 += self.__tube.first_collimator.thickness
        x2 += self.__tube.second_collimator.thickness

        first_coeffs = numpy.linalg.solve(numpy.array([[x1, 1], [x2, 1]]), numpy.array([y1 + diam1 / 2, y2 - diam2 / 2]))
        second_coeffs = numpy.linalg.solve(numpy.array([[x1, 1], [x2, 1]]), numpy.array([y1 - diam1 / 2, y2 + diam2 / 2]))
        return first_coeffs, second_coeffs
 

class Reflections:
    def __init__(self, ctube: CollimationTube, telescope: Telescope):
        self.__ctube = ctube
        self.__telescope = telescope

    def get_lines(self, plane: str) -> list[list[numpy.ndarray]]:
        lines = 10

        c1 = self.__ctube.first_collimator
        c2 = self.__ctube.second_collimator

        starting_x = c1.x_position
        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness, lines)
        stopping_x = self.__telescope.detector.x_position

        if plane == 'xy':
            starting_ceil = c1.y_position + c1.diameter / 2
            starting_floor = c1.y_position - c1.diameter / 2

            reflecting_ceil = (c2.y_position + c2.diameter / 2) * numpy.ones_like(reflecting_xs)
            reflecting_floor = (c2.y_position - c2.diameter / 2) * numpy.ones_like(reflecting_xs)

        if plane == 'xz':
            starting_ceil = c1.z_position + c1.diameter / 2
            starting_floor = c1.z_position - c1.diameter / 2

            reflecting_ceil = (c2.z_position + c2.diameter / 2) * numpy.ones_like(reflecting_xs)
            reflecting_floor = (c2.z_position - c2.diameter / 2) * numpy.ones_like(reflecting_xs)

        reflections = []
        for i in range(lines):
            reflections.append(self.__reflections_by(
                (starting_x, starting_ceil),
                (reflecting_xs[i], reflecting_floor[i]),
                stopping_x
            ))

        for i in range(lines):
            reflections.append(self.__reflections_by(
                (starting_x, starting_floor),
                (reflecting_xs[i], reflecting_ceil[i]),
                stopping_x
            ))

        return reflections

    def __reflections_by(self, start: tuple[float, float], reflect: tuple[float, float], stop_x: float) -> list[numpy.ndarray]:
        start_x, start_y = start
        reflect_x, reflect_y = reflect

        systematrix = numpy.array([[start_x, 1], [reflect_x, 1]])
        right_hand = numpy.array([start_y, reflect_y])
        coeffs = numpy.linalg.solve(systematrix, right_hand)

        ingoing_xs = numpy.array([start_x, reflect_x])
        outgoing_xs = numpy.array([reflect_x, stop_x])

        ingoing_ys = coeffs[0] * ingoing_xs + coeffs[1]
        outgoing_ys = -coeffs[0] * outgoing_xs + coeffs[0] * reflect[0] + reflect[1]

        return [ingoing_xs, ingoing_ys, outgoing_xs, outgoing_ys]


class Geometry:
    def __init__(self, chamber: Chamber) -> None:
        self.__chamber = chamber

    @property
    def chamber(self) -> Chamber:
        return self.__chamber

    @staticmethod
    def projection_formula(l1: float, h1: float, l2: float) -> float:
        return h1 * (l2 / l1)
    
    def spot_at_position(self, position: float) -> float:
        h1 = self.__chamber.ctube.first_collimator.diameter
        h2 = self.__chamber.ctube.second_collimator.diameter
        l0 = self.__chamber.ctube.length
        
        l1 = l0 - h1 * l0 / (h1 + h2)
        l2 = l0 - l1
        l3 = (position - self.__chamber.ctube.first_collimator.x_position) - l1

        return Geometry.projection_formula(l2, h2, l3)
    
    def spot_on_target(self) -> float:
        return self.spot_at_position(self.__chamber.target.x_position)

    def spot_on_detector(self) -> list[float]:
        positions = [self.__chamber.telescopes[i].detector.x_position for i in range(len(self.__chamber.telescopes))]
        return [self.spot_at_position(positions[i]) for i in range(len(positions))]
    
    def angle_resolution(self) -> list[float]:
        spots = self.spot_on_detector()
        scale = []

        for i in range(len(self.__chamber.telescopes)):
            scale.append(360 / (2 * numpy.pi * abs(self.__chamber.telescopes[i].detector.x_position - self.__chamber.target.x_position)))

        return [scale[i] * spots[i] for i in range(len(spots))]
    
    def collimator_optics(self, plane: str = 'xy') -> list[list[numpy.ndarray]]:
        ctube_optics = Optics(self.__chamber.ctube)
        return ctube_optics.get_lines(self.chamber.target.x_position, plane)
    
    def collimator_reflections(self, plane: str = 'xy') -> list[list[numpy.ndarray]]:
        ctube_reflections = Reflections(self.chamber.ctube, self.chamber.telescopes[0])
        return ctube_reflections.get_lines(plane)

    def telescope_optics(self) -> list[list[list[float]]]:
        result = []

        for telescope in self.__chamber.telescopes:
            tele_optics = Optics(telescope)
            coeffs = tele_optics.get_coefficients('xy')
            stop = self.find_stop_point(telescope, coeffs[0])
            result.append(tele_optics.get_lines(stop))

        return result
    
    def find_stop_point(self, telescope: Telescope, line_coefficients: numpy.ndarray) -> float:
        dx, dy = telescope.detector.x_position, telescope.detector.y_position
        eq_coeffs = [1 + line_coefficients[0]**2, 2 * line_coefficients[0] * line_coefficients[1], line_coefficients[1]**2 - (self.__chamber.diameter / 2)**2]

        x_lim = numpy.roots(eq_coeffs)
        y_lim = line_coefficients[0] * x_lim + line_coefficients[1]

        return x_lim[numpy.sqrt((x_lim - dx)**2 + (y_lim - dy)**2).argmax()]


if __name__ == '__main__':
    pass
