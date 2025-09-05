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
        if plane is None or plane.lower() not in ['xy', 'xz']:
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
        # first collimator
        for c in self.model.collimators:
            c.draw(self.axis, self.current_plane)

        # target
        self.model.target.draw(self.axis, self.current_plane)

        # detector
        self.model.detector.draw(self.axis, self.current_plane)

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
    
    def draw_collimator_optics(self) -> None:
        if self.current_plane == 'xy':
            coordinates = self.model.collimator_optics('xy')

        if self.current_plane == 'xz':
            coordinates = self.model.collimator_optics('xz')

        self.axis.scatter(coordinates[0], coordinates[1], color='black')
        
        self.axis.plot([coordinates[0][0], coordinates[0][-1], coordinates[1][0], coordinates[1][-1]], color='red', label='optics scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-2]], [coordinates[1][1], coordinates[1][-2]], color='red')

    def draw_telescope_optics(self) -> None:
        if self.current_plane == 'xy':
            coordinates = self.model.telescope_optics('xy')

        if self.current_plane == 'xz':
            coordinates = self.model.telescope_optics('xz')

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
