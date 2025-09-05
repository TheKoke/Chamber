import numpy
from backend.environment import *


class Chamber:
    def __init__(self, ctube: CollimationTube, trgt: Target, telescopes: list[Telescope]) -> None:
        self.__ctube = ctube
        self.__target = trgt
        self.__telescopes = telescopes

        detectors = [telescopes[i].detector for i in range(len(telescopes))]
        self.__pivots: list[Environment] = [self.__ctube.first_collimator, self.__ctube.second_collimator, self.__target, *detectors]

    @property
    def target(self) -> Target:
        return self.__target
    
    @property
    def ctube(self) -> CollimationTube:
        return self.__ctube
    
    @property
    def telescopes(self) -> list[Telescope]:
        return self.__telescopes


class Optics:
    def __init__(self, tube: Tube) -> None:
        self.__tube = tube

    @property
    def tube(self) -> Tube:
        return self.__tube
    
    def get_coefficients(self, plane: str = "xy") -> tuple[numpy.ndarray, numpy.ndarray]:
        if plane == "xy":
            theta_rad = self.__tube.theta * numpy.pi / 180
            r1, r2 = self.__tube.first_collimator.radius, self.__tube.second_collimator.radius
            x1, x2 = self.__tube.first_collimator.x_position, self.__tube.second_collimator.x_position
            y1, y2 = self.__tube.first_collimator.y_position, self.__tube.second_collimator.y_position

            xcenter1 = x1 * numpy.cos(theta_rad) - y1 * numpy.sin(theta_rad)
            ycenter1 = x1 * numpy.sin(theta_rad) + y1 * numpy.cos(theta_rad)

            xcenter2 = x2 * numpy.cos(theta_rad) - y2 * numpy.sin(theta_rad)
            ycenter2 = x2 * numpy.sin(theta_rad) + y2 * numpy.cos(theta_rad)

            x1 = xcenter1 + r1 * numpy.sin(theta_rad) / 2
            x2 = xcenter2 - r2 * numpy.sin(theta_rad) / 2
            y1 = ycenter1 + r1 * numpy.cos(theta_rad) / 2
            y2 = ycenter2 - r2 * numpy.cos(theta_rad) / 2

        if plane == "xz":
            x1, x2 = self.__tube.first_collimator.x_position, self.__tube.second_collimator.x_position
            y1, y2 = self.__tube.first_collimator.y_position, self.__tube.second_collimator.y_position

        first_coeffs = numpy.linalg.solve(numpy.array([[x1, 1], [x2, 1]]), numpy.array([y1, y2]))
        return first_coeffs, -first_coeffs
 

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
        h1 = self.__chamber.ctube.first_collimator.radius
        h2 = self.__chamber.ctube.second_collimator.radius
        
        crossing_h = self.__chamber.ctube.second_collimator.x_position - h1 * self.__chamber.ctube.second_collimator.x_position / (h1 + h2)
        d1 = self.__chamber.ctube.second_collimator.x_position - crossing_h

        return Geometry.projection_formula(d1, h2, distance - crossing_h)
    
    def spot_on_target(self) -> float:
        return self.spot_at_distance(self.__chamber.target.x_position)

    def spot_on_detector(self) -> float:
        return self.spot_at_distance(self.__chamber.telescopes[i].detector.x_position for i in range(len(self.__chamber.telescopes)))
    
    def angle_resolution(self) -> float:
        for i in range(len(self.__chamber.telescopes)):
            angle_scale = 360 / (2 * numpy.pi * (self.__chamber.telescopes[i].detector.x_position - self.__chamber.target.x_position))

        return angle_scale * self.spot_on_detector() / 2
    
    def collimator_optics(self, plane: str) -> list[list[float]]:
        ctube_optics = Optics(self.__chamber.ctube)
        first_coeffs, second_coeffs = ctube_optics.get_coefficients(plane)

        xs = self.__chamber.ctube.x_positions()
        ys = []

        for i in range(len(xs)):
            ys.append(first_coeffs[0] * xs[i] + first_coeffs[1])
            ys.append(second_coeffs[0] * xs[i] + second_coeffs[1])
        
        return [xs, ys]

    def telescope_optics(self, plane: str) -> list[list[list[float]]]:
        result = []

        for i in range(len(self.__chamber.telescopes)):
            tele_optics = Optics(self.__chamber.telescopes[i])
            first_coeffs, second_coeffs = tele_optics.get_coefficients(plane)

            xs = self.__chamber.telescopes[i].x_positions()
            ys = []

            for j in range(len(xs)):
                ys.append(first_coeffs[0] * xs[i] + first_coeffs[1])
                ys.append(second_coeffs[0] * xs[i] + second_coeffs[1])
            
            result.append([xs, ys])

        return result




if __name__ == '__main__':
    pass
