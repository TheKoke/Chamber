import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle


class Geometry:
    '''
              F 
             /|
        A  C/ | 
        |\ /| |
        | X | |
        |/ \| |
        B  D\ |
             \|
        B' D' G

    Intersection dot => O
    AB = H1
    CD = H2
    FG - ?

    B'D' = D1
    D'G = D2
    '''

    def __init__(self, h1: float, h2: float, d1: float, d2: float, d3: float, t1: float = 2.0, t2: float = 2.0) -> None:
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

    def find_second_distance(self) -> float:
        return self.d1 - self.h1 * self.d1 / (self.h1 + self.h2)
    
    def find_spot_radius(self) -> float:
        return self.h2 * (self.find_second_distance() + self.d2 - self.t2) / self.find_second_distance()
    
    def find_detector_size(self) -> float:
        return self.h2 * (self.find_second_distance() + self.d2 + self.d3 - self.t2) / self.find_second_distance()
    
    def build_coordinates(self) -> list[list[float]]:
        distances = [0, self.d1, self.d2, self.d3]
        heights = [self.h1, self.h2, self.find_spot_radius(), self.find_detector_size()]

        dots = [[], []]
        for i in range(4):
            dots[0].append(sum(distances[:i + 1]))
            dots[0].append(sum(distances[:i + 1]))

        for i in range(4):
            dots[1].append(-heights[i] / 2)
            dots[1].append(heights[i] / 2)

        return dots


class Stereometry(Geometry):
    def __init__(self, h1: float, h2: float, d1: float, d2: float, d3: float, t1: float = 2, t2: float = 2) -> None:
        super().__init__(h1, h2, d1, d2, d3, t1, t2)


class Painter:
    def __init__(self, axes: Axes, model: Geometry | Stereometry) -> None:
        self.axes = axes
        self.model = model
        self._is_env_exist = False

    def draw_all_environment(self) -> None:
        self._is_env_exist = True
        dots = self.model.build_coordinates()
        collimator_height = 20.0

        self.axes.plot([0, dots[0][-1]], [0, 0], '--', color='red', label='beam line')
        self.axes.scatter(dots[0], dots[1], color='black')

        # collimators
        self.__add_collimator(
            (dots[0][0], dots[1][0] - (collimator_height - self.model.h1) / 2), 
            self.model.t1 * 10, 
            self.model.h1, 
            collimator_height
        )

        self.__add_collimator(
            (dots[0][2], dots[1][2] - (collimator_height - self.model.h2) / 2), 
            self.model.t2 * 10, 
            self.model.h2, 
            collimator_height
        )

        self.axes.plot([dots[0][4], dots[0][5]], [dots[1][4] - 3.0, dots[1][5] + 3.0], color='purple', label='target') # target
        self.__add_arc() # detector angles
        self.__add_detector(dots[0][-1] + 10, 3.0) # detector

    def draw_reflections(self) -> None:
        dots = self.model.build_coordinates()

        if not self._is_env_exist:
            self.draw_all_environment()

        self.reflections_lines((dots[0][0], dots[1][0]), (dots[0][3], dots[1][3]))
        self.reflections_lines((dots[0][1], dots[1][1]), (dots[0][2], dots[1][2]))

        self.axes.set_title('Vertical View')
        self.axes.grid()
        self.axes.legend()

    def reflections_lines(self, first_border: tuple[float, float], second_border: tuple[float, float], num: int = 10) -> None:
        systematrix = np.array([[first_border[0], 1], [second_border[0], 1]])
        righthand = np.array([first_border[1], second_border[1]])
        coeffs = np.linalg.solve(systematrix, righthand)

        for i in range(num + 1):
            xs = np.linspace(first_border[0] + self.model.t1 * i, second_border[0] + self.model.t1 * i, 3)
            ys = coeffs[0] * xs + (first_border[1] - self.model.t1 * i * coeffs[0])
            self.axes.plot(xs, ys, color='green')

        for i in range(num + 1):
            xs = np.linspace(second_border[0] + self.model.t1 * i, 1.65 * second_border[0], 3)
            ys = -coeffs[0] * xs + (np.sign(second_border[1]) * self.model.h2 + second_border[1] + self.model.t1 * i * coeffs[0])
            self.axes.plot(xs, ys, color='green')

    def draw_optic_3d(self) -> None:
        if not self.model.__class__ == Stereometry:
            return

    def draw_optic_2d(self) -> None:
        if not self.model.__class__ == Geometry:
            return
        
        if not self._is_env_exist:
            self.draw_all_environment()
        
        dots = self.model.build_coordinates()

        self.axes.plot([dots[0][0], dots[0][-1]], [dots[1][0], dots[1][-1]], color='red') # bounds of scatter
        self.axes.plot([dots[0][1], dots[0][-2]], [dots[1][1], dots[1][-2]], color='red')
        
        self.axes.set_title('Vertical View')
        self.axes.grid()
        self.axes.legend()

    def __add_arc(self) -> None:
        ys = np.linspace(10, -10, 20)
        xs = np.sqrt(self.model.d3 ** 2 - ys ** 2) + (self.model.d1 + self.model.d2)

        mm_per_degree = 3.837
        
        degrees = np.hstack([np.arange(0, ys.min(), -mm_per_degree), np.arange(0, ys.max(), mm_per_degree)])
        scats = np.sqrt(self.model.d3 ** 2 - degrees ** 2) + (self.model.d1 + self.model.d2)

        self.axes.scatter(scats, degrees, marker='_', color='black')
        self.axes.plot(xs, ys, color='black')

    def __add_collimator(self, xy: tuple[float, float], thickness: float, radius: float, height: float) -> None:
        height = (height - radius) / 2
        self.axes.add_patch(Rectangle(xy, thickness, height, color='black', label='collimator'))
        self.axes.add_patch(Rectangle((xy[0], xy[1] + height + radius), thickness, height, color='black'))

    def __add_detector(self, x: float, height: float) -> None:
        self.axes.add_patch(Rectangle((x, -height / 2), 70, height, color='blue', label='detector'))
    


if __name__ == '__main__':
    fig, ax = plt.subplots()

    g = Geometry(3, 3, 960, 360, 220)
    p = Painter(ax, g)

    p.draw_reflections()
    plt.show()