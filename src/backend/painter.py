from geometry import Geometry

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, Arc


class Painter:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

        self.is_optics_enable = True
        self.is_reflections_enable = False

    def draw(self, plane: str) -> None:
        if plane.lower() not in ['xy', 'xz', 'yz']:
            plane = 'xy'

        self.axis.clear()

        self.draw_environment(plane)

        xmin, xmax = self.axis.get_xlim()
        self.axis.plot([xmin, xmax], [0, 0], '--', color='red', label='beam line')

        if self.is_optics_enable:
            self.draw_optics(plane)

        if self.is_reflections_enable:
            self.draw_reflections(plane)

    def draw_environment(self, plane: str) -> None:
        if plane == 'xy':
            # first collimator
            c1 = self.model.first_collimator
            self.__add_collimator(c1.x_position, c1.y_position, c1.radius, c1.thickness, c1.height)

            # last collimator
            c2 = self.model.last_collimator
            self.__add_collimator(c2.x_position, c2.y_position, c2.radius, c2.thickness, c2.height)

            # target
            t = self.model.target
            self.__add_target(t.x_position, t.y_position, t.width)

            # detector
            d = self.model.detector
            self.__add_detector(d.x_position, d.y_position)

        if plane == 'xz':
            # first collimator
            c1 = self.model.first_collimator
            self.__add_collimator(c1.x_position, c1.z_position, c1.radius, c1.thickness, c1.height)

            # last collimator
            c2 = self.model.last_collimator
            self.__add_collimator(c2.x_position, c2.z_position, c2.radius, c2.thickness, c2.height)

            # target
            t = self.model.target
            self.__add_target(t.x_position, t.z_position, t.height)

            # detector
            d = self.model.detector
            self.__add_detector(d.x_position, d.z_position)

        if plane == 'yz':
            # first collimator
            c1 = self.model.first_collimator
            self.__add_collimator(c1.y_position, c1.z_position, c1.radius, c1.thickness, c1.height)

            # last collimator
            c2 = self.model.last_collimator
            self.__add_collimator(c2.y_position, c2.z_position, c2.radius, c2.thickness, c2.height)

            # target
            t = self.model.target
            self.__add_target(t.y_position, t.z_position, t.width)

            # detector
            d = self.model.detector
            self.__add_detector(d.y_position, d.z_position)

    def __add_collimator(self, axis_x: float, axis_y: float, radius: float, thickness: float, height: float) -> None:
        self.axis.add_patch(Rectangle(
            (axis_x, axis_y + radius / 2), thickness * 10, height / 2 - radius, color='black', label='collimator'
        ))

        self.axis.add_patch(Rectangle(
            (axis_x, axis_y - height / 2 + radius / 2), thickness * 10, height / 2 - radius, color='black'
        ))

    def __add_target(self, axis_x: float, axis_y: float, height: float) -> None:
        self.axis.plot([axis_x, axis_x], [axis_y - height / 2, axis_y + height / 2], color='purple', label='target')

    def __add_detector(self, axis_x: float, axis_y: float) -> None:
        DETECTOR_WIDTH = 12.0
        self.axis.add_patch(Rectangle(
            (axis_x, axis_y - DETECTOR_WIDTH / 20), DETECTOR_WIDTH * 10, DETECTOR_WIDTH / 10, color='blue', label='detector'
        ))
        
        x0, y0 = self.model.target.x_position, self.model.target.y_position
        radii = self.model.detector.x_position - self.model.target.x_position
        self.axis.add_patch(Arc((x0, y0), 2 * radii, 2 * radii, theta1=-10, theta2=10, linestyle='-.'))

    def draw_optics(self, plane: str) -> None:
        if plane == 'xy':
            coordinates = self.model.xy_plane()

        if plane == 'xz':
            coordinates = self.model.xz_plane()

        if plane == 'yz':
            coordinates = self.model.yz_plane()

        self.axis.scatter(coordinates[0], coordinates[1], color='black')

        self.axis.plot([coordinates[0][0], coordinates[0][-1]], [coordinates[1][0], coordinates[1][-1]], color='red', label='optic scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-2]], [coordinates[1][1], coordinates[1][-2]], color='red')

    def draw_reflections(self, plane: str) -> None:
        if plane == 'xy':
            reflections = self.model.xy_reflections()

        if plane == 'xz':
            reflections = self.model.xz_reflections()

        if plane == 'yz':
            reflections = self.model.yz_reflections()

    def switch_enable_optics(self) -> None:
        self.is_optics_enable = not self.is_optics_enable
        self.draw()

    def switch_enable_reflections(self) -> None:
        self.is_reflections_enable = not self.is_reflections_enable
        self.draw()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from start import starting_position
    
    fig, ax = plt.subplots()

    geom = starting_position()
    paint = Painter(ax, geom)

    paint.draw('xy')

    ax.grid()
    ax.set_ylim(-10, 10)
    ax.set_xlim((-20, 1700))
    ax.legend()
    plt.show()
