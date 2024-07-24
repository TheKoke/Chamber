from backend.geometry import Geometry

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, Arc


SCOPING = 10


class Painter:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

        self.current_plane = None
        self.is_optics_enable = False
        self.is_reflections_enable = False

        self.draw(self.current_plane)

    def draw(self, plane: str) -> None:
        if plane is None or plane.lower() not in ['xy', 'xz', 'yz']:
            plane = 'xy'

        self.current_plane = plane

        self.axis.clear()

        self.draw_environment()

        xmin, xmax = self.axis.get_xlim()
        self.axis.plot([xmin, xmax], [0, 0], '--', color='red', label='beam line')

        if self.is_optics_enable:
            self.draw_optics()

        if self.is_reflections_enable:
            self.draw_reflections()

        self.axis.set_title(f'{self.current_plane.upper()} Plane View of Chamber')
        self.axis.grid()
        self.axis.legend()

    def draw_environment(self) -> None:
        if self.current_plane == 'xy':
            # first collimator
            c1 = self.model.__first_collimator
            self.__add_collimator(c1.x_position, c1.y_position, c1.radius, c1.thickness, c1.height)

            # last collimator
            c2 = self.model.__last_collimator
            self.__add_collimator(c2.x_position, c2.y_position, c2.radius, c2.thickness, c2.height)

            # target
            t = self.model.__target
            self.__add_target(t.x_position, t.y_position, t.width)

            # detector
            d = self.model.__detector
            self.__add_detector(d.x_position, d.y_position)

        if self.current_plane == 'xz':
            # first collimator
            c1 = self.model.__first_collimator
            self.__add_collimator(c1.x_position, c1.z_position, c1.radius, c1.thickness, c1.height)

            # last collimator
            c2 = self.model.__last_collimator
            self.__add_collimator(c2.x_position, c2.z_position, c2.radius, c2.thickness, c2.height)

            # target
            t = self.model.__target
            self.__add_target(t.x_position, t.z_position, t.height)

            # detector
            d = self.model.__detector
            self.__add_detector(d.x_position, d.z_position)

        if self.current_plane == 'yz':
            # first collimator
            c1 = self.model.__first_collimator
            self.__add_collimator(c1.y_position, c1.z_position, c1.radius, c1.thickness, c1.height)

            # last collimator
            c2 = self.model.__last_collimator
            self.__add_collimator(c2.y_position, c2.z_position, c2.radius, c2.thickness, c2.height)

            # target
            t = self.model.__target
            self.__add_target(t.y_position, t.z_position, t.width)

            # detector
            d = self.model.__detector
            self.__add_detector(d.y_position, d.z_position)

    def __add_collimator(self, axis_x: float, axis_y: float, radius: float, thickness: float, height: float) -> None:
        self.axis.add_patch(Rectangle(
            (axis_x, axis_y + radius / 2), thickness * SCOPING, height / 2 - radius, color='black', label='collimator'
        ))

        self.axis.add_patch(Rectangle(
            (axis_x, axis_y - height / 2 + radius / 2), thickness * SCOPING, height / 2 - radius, color='black'
        ))

    def __add_target(self, axis_x: float, axis_y: float, height: float) -> None:
        self.axis.plot([axis_x, axis_x], [axis_y - height / 2, axis_y + height / 2], color='purple', label='target')

    def __add_detector(self, axis_x: float, axis_y: float) -> None:
        DETECTOR_WIDTH = 12.0
        self.axis.add_patch(Rectangle(
            (axis_x, axis_y - DETECTOR_WIDTH / (2 * SCOPING)), 
            DETECTOR_WIDTH * SCOPING, 
            DETECTOR_WIDTH / SCOPING, 
            color='blue', 
            label='detector'
        ))
        
        x0, y0 = self.model.__target.x_position, self.model.__target.y_position
        radii = self.model.__detector.x_position - self.model.__target.x_position
        self.axis.add_patch(Arc((x0, y0), 2 * radii, 2 * radii, theta1=-5, theta2=5, linestyle='-.'))

    def draw_optics(self) -> None:
        if self.current_plane == 'xy':
            coordinates = self.model.xy_optics()

        if self.current_plane == 'xz':
            coordinates = self.model.xz_optics()

        if self.current_plane == 'yz':
            coordinates = self.model.yz_optics()

        self.axis.scatter(coordinates[0], coordinates[1], color='black')

        self.axis.plot([coordinates[0][0], coordinates[0][-1]], [coordinates[1][0], coordinates[1][-1]], color='red', label='optic scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-2]], [coordinates[1][1], coordinates[1][-2]], color='red')

    def draw_reflections(self) -> None:
        if self.current_plane == 'xy':
            reflections = self.model.xy_reflections()

        if self.current_plane == 'xz':
            reflections = self.model.xz_reflections()

        if self.current_plane == 'yz':
            reflections = self.model.yz_reflections()

        for refl in reflections[:-1]:
            xs, ys = refl
            self.axis.plot(xs, ys, color='green')

        self.axis.plot(reflections[-1][0], reflections[-1][1], color='green', label='reflections')

    def switch_optics(self) -> None:
        self.is_optics_enable = not self.is_optics_enable
        self.draw(self.current_plane)

    def switch_reflections(self) -> None:
        self.is_reflections_enable = not self.is_reflections_enable
        self.draw(self.current_plane)

    def add_pointer(self, x: float) -> None:
        pass


if __name__ == '__main__':
    pass
