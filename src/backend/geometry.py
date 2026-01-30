import numpy
from backend.environment import *


class Optics:
    def __init__(self, tube: Tube) -> None:
        self.__tube = tube

    @property
    def tube(self) -> Tube:
        return self.__tube
    
    def get_coefficients(self, plane: str = "xy") -> tuple[numpy.ndarray, numpy.ndarray]:
        if plane == "xy":
            diam1, diam2 = self.__tube.first_collimator.diameter, self.__tube.second_collimator.diameter
            x1, x2 = self.__tube.first_collimator.x_position, self.__tube.second_collimator.x_position
            y1, y2 = self.__tube.first_collimator.y_position, self.__tube.second_collimator.y_position

            # x1 += diam1 / 2 * numpy.sin(numpy.radians(self.__tube.theta)) / 2
            # x2 -= diam2 / 2 * numpy.sin(numpy.radians(self.__tube.theta)) / 2
            y1 += diam1 / 2 # * numpy.cos(numpy.radians(self.__tube.theta)) / 2
            y2 -= diam2 / 2 # * numpy.cos(numpy.radians(self.__tube.theta)) / 2

        if plane == "xz":
            x1, x2 = self.__tube.first_collimator.x_position, self.__tube.second_collimator.x_position
            y1, y2 = self.__tube.first_collimator.z_position, self.__tube.second_collimator.z_position

        first_coeffs = numpy.linalg.solve(numpy.array([[x1, 1], [x2, 1]]), numpy.array([y1, y2]))
        return first_coeffs, -first_coeffs
 

class Reflections:
    def __init__(self, first: Collimator, second: Collimator, target: Target, telescope: Telescope):
        self.__first = first
        self.__second = second
        self.__target = target
        self.__telescope = telescope

    def get_coefficients(self, plane: str) -> list[tuple[numpy.ndarray, numpy.ndarray]]:
        lines = 10

        c1 = self.__first
        c2 = self.__second

        starting_x = c1.x_position

        starting_ceil_y = c1.y_position + c1.diameter / 2
        starting_floor_y = c1.y_position - c1.diameter / 2

        reflecting_xs = numpy.linspace(c2.x_position, c2.x_position + c2.thickness, lines) # numpy.linspace(0, 1, 10) => [0.0, 0.1, 0.2, 0.3,...,1.0]

        reflecting_floor_ys = (c2.y_position - c2.diameter / 2) * numpy.ones_like(reflecting_xs)
        reflecting_ceil_ys = (c2.y_position + c2.diameter / 2) * numpy.ones_like(reflecting_xs)

        stopping_x = self.__telescope.detector_position[0]

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


class Geometry:
    def __init__(self, chamber: Chamber) -> None:
        self.__chamber = chamber

    @property
    def chamber(self) -> Chamber:
        return self.__chamber

    @staticmethod
    def projection_formula(d1: float, h1: float, d2: float) -> float:
        return h1 * (d2 / d1)
    
    def spot_at_distance(self, distance: float) -> float:
        h1 = self.__chamber.ctube.first_collimator.diameter
        h2 = self.__chamber.ctube.second_collimator.diameter
        
        crossing_h = self.__chamber.ctube.second_collimator.x_position - h1 * self.__chamber.ctube.second_collimator.x_position / (h1 + h2)
        d1 = self.__chamber.ctube.second_collimator.x_position - crossing_h

        return Geometry.projection_formula(d1, h2, distance - crossing_h)
    
    def spot_on_target(self) -> float:
        return self.spot_at_distance(self.__chamber.target.x_position)

    def spot_on_detector(self) -> float:
        return self.spot_at_distance(self.__chamber.telescopes[i].detector_position[0] for i in range(len(self.__chamber.telescopes)))
    
    def angle_resolution(self) -> float:
        for i in range(len(self.__chamber.telescopes)):
            angle_scale = 360 / (2 * numpy.pi * (self.__chamber.telescopes[i].detector_position[0] - self.__chamber.target.x_position))

        return angle_scale * self.spot_on_detector() / 2
    
    def collimator_optics(self) -> list[list[float]]:
        ctube_optics = Optics(self.__chamber.ctube)
        first_coeffs, second_coeffs = ctube_optics.get_coefficients()

        xs = self.__chamber.ctube.x_positions()
        ys = []

        for i in range(len(xs)):
            ys.append(first_coeffs[0] * xs[i] + first_coeffs[1])
            ys.append(second_coeffs[0] * xs[i] + second_coeffs[1])
        
        return [xs * 2, ys]

    def telescope_optics(self) -> list[list[list[float]]]:
        result = []

        for telescope in self.__chamber.telescopes:
            dx, dy, dz = telescope.detector_position

            tele_optics = Optics(telescope)
            first_coeffs, second_coeffs = tele_optics.get_coefficients()

            eq_coeffs1 = [1 + first_coeffs[0]**2, 2 * first_coeffs[0] * first_coeffs[1], first_coeffs[1]**2 - (self.__chamber.diameter / 2)**2]
            eq_coeffs2 = [1 + second_coeffs[0]**2, 2 * second_coeffs[0] * second_coeffs[1], second_coeffs[1]**2 - (self.__chamber.diameter / 2)**2]

            x_lim1 = numpy.roots(eq_coeffs1)
            y_lim1 = first_coeffs[0] * x_lim1 + first_coeffs[1]

            x_lim2 = numpy.roots(eq_coeffs2)
            y_lim2 = second_coeffs[0] * x_lim2 + second_coeffs[1]

            true_x1 = x_lim1[numpy.sqrt((x_lim1 - dx)**2 + (y_lim1 - dy)**2).argmax()]
            true_y1 = y_lim1[numpy.sqrt((x_lim1 - dx)**2 + (y_lim1 - dy)**2).argmax()]

            true_x2 = x_lim2[numpy.sqrt((x_lim2 - dx)**2 + (y_lim2 - dy)**2).argmax()]
            true_y2 = y_lim2[numpy.sqrt((x_lim2 - dx)**2 + (y_lim2 - dy)**2).argmax()]

            xs = [*telescope.x_positions(), *telescope.x_positions(), true_x1, true_x2]
            ys = [true_y1, true_y2]

            for i in range(0, len(telescope.x_positions())):
                ys.insert(0, first_coeffs[0] * xs[i] + first_coeffs[1])
                ys.insert(0, second_coeffs[0] * xs[i] + second_coeffs[1])
            
            result.append([xs, ys])

        return result
    
if __name__ == '__main__':
    pass
