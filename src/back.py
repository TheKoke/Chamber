import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, Ellipse


def draw_ellipse(axis: Axes, r1: float, r2: float, shift_1: float, shift_2: float) -> None:
    d = np.sqrt(shift_1 ** 2 + shift_2 ** 2)

    s = (r1 + r2 + d) / 2
    width = (r1 + r2 - d)

    height = width
    if d != 0:
        height = 4 * np.sqrt(s * (s - r1) * (s - r2) * (s - d)) / d

    ang = 0
    if shift_1 != 0:
        ang += (np.tan(shift_2 / shift_1) - np.pi / 2) * 180 / np.pi

    axis.add_patch(Rectangle([-3.5, -3.5], 7, 7, color='purple', label='target'))
    axis.add_patch(Ellipse([0, 0], width, height, angle=ang, color='red', label='beam spot'))


class Geometry:
    '''
         /|
        / | 
    |\ /| |
    | X | |
    |/ \| |
        \ |
         \|
    '''

    ENVIRONMENT_COUNT = 4

    def __init__(self, h1: float, h2: float, d1: float, d2: float, d3: float, t1: float = 2.0, t2: float = 2.0, view: str = 'h') -> None:
        """
        h1 = radius of 1st collimator,\n
        h2 = radius of 2nd collimator,\n
        t1 = thickness of 1st collimator,\n
        t2 = thickness of 2nd collimator,\n
        d1 = distance between two collimators,\n
        d2 = distance between 2nd collimator and target,\n
        d3 = distance between target and detector,
        """
        self.h1 = h1
        self.h2 = h2
        self.t1 = t1
        self.t2 = t2

        self.d1 = d1
        self.d2 = d2
        self.d3 = d3

        self.view = view

        self.coordinates = self.build_coordinates()

    def find_second_distance(self) -> float:
        return self.d1 - self.h1 * self.d1 / (self.h1 + self.h2)
    
    def calc_spot_radius(self) -> float:
        return self.h2 * (self.find_second_distance() + self.d2 - self.t2) / self.find_second_distance()
    
    def calc_detector_size(self) -> float:
        return self.h2 * (self.find_second_distance() + self.d2 + self.d3 - self.t2) / self.find_second_distance()
    
    def calc_minimum_angle(self) -> float:
        scale_value =  360 / (2 * np.pi * self.d3)
        return scale_value * self.calc_detector_size() / 2
    
    def build_coordinates(self) -> list[list[float]]:
        distances = [0, self.d1, self.d2, self.d3]
        heights = [self.h1, self.h2, self.calc_spot_radius(), self.calc_detector_size()]

        dots = [[], []]
        for i in range(self.ENVIRONMENT_COUNT): # x-coordinates
            dots[0].append(sum(distances[:i + 1]))
            dots[0].append(sum(distances[:i + 1]))

        for i in range(self.ENVIRONMENT_COUNT): # y-coordinates
            dots[1].append(-heights[i] / 2)
            dots[1].append(heights[i] / 2)

        return dots
    
    def rebuild(self) -> None:
        heights = [self.h1, self.h2]
        dots = [self.coordinates[0], self.coordinates[1][:4]]

        first_coeffs = np.linalg.solve(np.array([[dots[0][0], 1], [dots[0][3], 1]]), np.array([dots[1][0], dots[1][3]]))
        sec_coeffs = np.linalg.solve(np.array([[dots[0][1], 1], [dots[0][2], 1]]), np.array([dots[1][1], dots[1][2]]))

        for i in range(len(heights), 4):
            dots[1].append(sec_coeffs[0] * dots[0][i * 2]  + sec_coeffs[1])
            dots[1].append(first_coeffs[0] * dots[0][i * 2] + first_coeffs[1])

        self.coordinates = dots
    
    def shift_dots(self, object_index: int, direction: str, val: float) -> None:
        possible_directions = ['up', 'down'] if self.view == 'v' else ['right', 'left']

        if object_index < 0 or object_index >= self.ENVIRONMENT_COUNT:
            return

        if direction not in possible_directions:
            return
        
        if direction == 'up' or direction == 'right':
            self.coordinates[1][object_index * 2] += val
            self.coordinates[1][object_index * 2 + 1] += val

        if direction == 'down' or direction == 'left':
            self.coordinates[1][object_index * 2] -= val
            self.coordinates[1][object_index * 2 + 1] -= val

class Painter:

    DETECTOR_WIDTH = 70
    ARC_HEIGHT = 20
    TARGET_HEIGHT = 14
    COLLIMATOR_HEIGHT = 20.0
    
    def __init__(self, axes: Axes, model: Geometry) -> None:
        self.axes = axes
        self.model = model

        self._is_env_exist = False
        self._is_optic_drawn = False
        self._is_reflections_drawn = False

    def draw_all_environment(self) -> None:
        self._is_env_exist = True
        dots = self.model.coordinates

        self.axes.scatter(dots[0], dots[1], color='black')

        # collimators
        self.__add_collimator(
            (dots[0][0], dots[1][0] - (self.COLLIMATOR_HEIGHT - self.model.h1) / 2), 
            self.model.t1 * 10, 
            self.model.h1, 
            self.COLLIMATOR_HEIGHT
        )

        self.__add_collimator(
            (dots[0][2], dots[1][2] - (self.COLLIMATOR_HEIGHT - self.model.h2) / 2), 
            self.model.t2 * 10, 
            self.model.h2, 
            self.COLLIMATOR_HEIGHT
        )

        self.__add_arc() # detector angles
        self.__add_detector(dots[0][-1] + 10, 3.0) # detector
        self.axes.plot([dots[0][4], dots[0][5]], [-self.TARGET_HEIGHT / 2, self.TARGET_HEIGHT / 2], color='purple', label='target') # target

        self.axes.plot([0, dots[0][-1]], [0, 0], '--', color='red', label='beam line')

    def draw_reflections(self) -> None:
        if self._is_reflections_drawn:
            return

        if not self._is_env_exist:
            self.draw_all_environment()

            self.axes.set_title('Vertical View' if self.model.view == 'v' else 'Horizonthal view')
            self.axes.grid()

        self._is_reflections_drawn = True
        dots = self.model.coordinates

        self.reflections_lines((dots[0][0], dots[1][0]), (dots[0][3], dots[1][3]))
        self.reflections_lines((dots[0][1], dots[1][1]), (dots[0][2], dots[1][2]))

        self.reflections_lines((dots[0][0] + self.model.t1 * 10, dots[1][0]), (dots[0][3], dots[1][3]), num=1, legend='reflections')
        self.reflections_lines((dots[0][1] + self.model.t1 * 10, dots[1][1]), (dots[0][2], dots[1][2]), num=1)

        self.axes.legend()

    def reflections_lines(self, first_border: tuple[float, float], second_border: tuple[float, float], num: int = 10, legend: str = '') -> None:
        systematrix = np.array([[first_border[0], 1], [second_border[0], 1]])
        righthand = np.array([first_border[1], second_border[1]])
        coeffs = np.linalg.solve(systematrix, righthand)

        first_step = self.model.t1 * 10 / num
        for i in range(num):
            xs = np.linspace(first_border[0] + first_step * i, second_border[0] + first_step * i, 3)
            ys = coeffs[0] * xs + (coeffs[1] - first_step * i * coeffs[0])
            self.axes.plot(xs, ys, color='green')
            if legend != '':
                self.axes.plot(xs, ys, color='green', label=legend)

        second_step = self.model.t2 * 10 / num
        for i in range(num):
            xs = np.linspace(second_border[0] + second_step * i, self.model.d1 + self.model.d2 + self.model.d3 + 15, 3)
            
            shift_coeff = second_border[1] + second_border[0] * coeffs[0]
            ys = -coeffs[0] * xs + (shift_coeff + second_step * i * coeffs[0])
            self.axes.plot(xs, ys, color='green')

    def draw_optic(self) -> None:
        if self._is_optic_drawn:
            return

        if not self._is_env_exist:
            self.draw_all_environment()

            self.axes.set_title('Vertical View' if self.model.view == 'v' else 'Horizonthal view')
            self.axes.grid()

        self._is_optic_drawn = True
        dots = self.model.coordinates

        self.axes.plot([dots[0][0], dots[0][-1]], [dots[1][0], dots[1][-1]], color='red', label='optic scatter') # bounds of scatter
        self.axes.plot([dots[0][1], dots[0][-2]], [dots[1][1], dots[1][-2]], color='red')

        self.axes.legend()

    def __add_arc(self) -> None:
        ys = np.linspace(-self.ARC_HEIGHT / 2, self.ARC_HEIGHT / 2, 20)
        xs = np.sqrt(self.model.d3 ** 2 - ys ** 2) + (self.model.d1 + self.model.d2)

        mm_per_degree = (2 * np.pi * self.model.d3) / 360
        
        degrees = np.hstack([np.arange(0, ys.min(), -mm_per_degree), np.arange(0, ys.max(), mm_per_degree)])
        scats = np.sqrt(self.model.d3 ** 2 - degrees ** 2) + (self.model.d1 + self.model.d2)

        self.axes.scatter(scats, degrees, marker='_', color='black')
        self.axes.plot(xs, ys, color='black')

    def __add_collimator(self, xy: tuple[float, float], thickness: float, radius: float, height: float) -> None:
        height = (height - radius) / 2
        self.axes.add_patch(Rectangle(xy, thickness, height, color='black', label='collimator'))
        self.axes.add_patch(Rectangle((xy[0], xy[1] + height + radius), thickness, height, color='black'))

    def __add_detector(self, x: float, height: float) -> None:
        self.axes.add_patch(Rectangle((x, -height / 2), self.DETECTOR_WIDTH, height, color='blue', label='detector'))


if __name__ == '__main__':
    fig, ax = plt.subplots()

    g = Geometry(3, 3, 960, 360, 220, view='v')
    p = Painter(ax, g)

    g.shift_dots(0, 'up', -2.0)
    g.rebuild()

    p.draw_optic()
    p.draw_reflections()
    plt.tight_layout()
    plt.show()