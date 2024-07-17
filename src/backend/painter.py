from backend.geometry import Geometry

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle


class Painter:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

        self.is_optics_enable = False
        self.is_reflections_enable = False

    def draw(self, plane: str) -> None:
        if plane.lower() not in ['xy', 'xz', 'yz']:
            plane = 'xy'

        self.axis.clear()

        self.draw_environment(plane)

        if self.is_optics_enable:
            self.draw_optics(plane)

        if self.is_reflections_enable:
            self.draw_reflections(plane)

    def draw_environment(self, plane: str) -> None:
        if plane == 'xy':
            coordinates = self.model.xy_plane()

        if plane == 'xz':
            coordinates = self.model.xz_plane()

        if plane == 'yz':
            coordinates = self.model.yz_plane()

        self.axis.add_patch(Rectangle(
            (coordinates[0][0], coordinates[1][0]),
            self.model.first_collimator.thickness,
            self.model.first_collimator.radius * 2,
        )) # first collimator
        self.axis.add_patch(Rectangle(
            (coordinates[0][1], coordinates[1][1] - self.model.first_collimator.radius * 2),
            self.model.first_collimator.thickness,
            self.model.first_collimator.radius * 2
        )) # first collimator

        self.axis.add_patch(Rectangle()) # last collimator
        self.axis.add_patch(Rectangle()) # last collimator

        self.axis.plot() # target

        self.axis.add_patch(Rectangle()) # detector
        self.axis.plot() # detector angles arc

    def draw_optics(self, plane: str) -> None:
        if plane == 'xy':
            coordinates = self.model.xy_plane()

        if plane == 'xz':
            coordinates = self.model.xz_plane()

        if plane == 'yz':
            coordinates = self.model.yz_plane()

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
    pass
