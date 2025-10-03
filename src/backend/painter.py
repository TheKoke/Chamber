from matplotlib.axes import Axes
from backend.geometry import Geometry, Optics, Reflections
from backend.environment import Collimator, Target, Telescope, CollimationTube


class FullPainter:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

        self.current_plane = None
        self.is_collimator_optics_enable = False
        self.is_telescope_optics_enable = False

        self.draw(self.current_plane)

    def draw(self, plane: str) -> None:
        if plane is None or plane.lower() not in ['xy', 'xz']:
            plane = 'xy'

        self.current_plane = plane

        self.axis.clear()

        self.draw_environment()

        xmin, xmax = self.axis.get_xlim()
        self.axis.plot([xmin, xmax], [0, 0], '--', color='red', label='beam line')

        if self.is_collimator_optics_enable:
            self.draw_collimator_optics()

        if self.is_telescope_optics_enable:
            self.draw_telescope_optics()

        self.axis.set_title(f'{self.current_plane.upper()} Plane View of Chamber')
        self.axis.grid()
        self.axis.legend()

    def draw_environment(self) -> None:
        self.model.chamber.ctube.draw(self.axis, self.current_plane)
        self.model.chamber.target.draw(self.axis, self.current_plane)
        
        for t in self.model.chamber.telescopes:
            t.draw(self.axis, self.current_plane)

    def draw_collimator_optics(self) -> None:
        coordinates = self.model.collimator_optics('xy')

        self.axis.scatter(coordinates[0], coordinates[1], color='black')
        
        self.axis.plot([coordinates[0][0], coordinates[0][-1]], [coordinates[1][0], coordinates[1][-1]], color='red', label='collim. scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-2]], [coordinates[1][1], coordinates[1][-2]], color='red')

    def draw_telescope_optics(self) -> None:
        coordinates = self.model.telescope_optics('xy')

        self.axis.scatter(coordinates[0], coordinates[1], color='blue')
        
        self.axis.plot([coordinates[0][0], coordinates[0][-1]], [coordinates[1][0], coordinates[1][-1]], color='purple', label='telesc. scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-2]], [coordinates[1][1], coordinates[1][-2]], color='purple')

    def switch_optics(self) -> None:
        self.is_optics_enable = not self.is_optics_enable
        self.draw(self.current_plane)

    def add_pointer(self, x: float) -> None:
        pass


class DetailedPainter:
    def __init__(self, axis: Axes, first: Collimator, second: Collimator, target: Target, telescope: Telescope) -> None:
        self.axis = axis
        self.first = first
        self.second = second
        self.target = target
        self.telescope = telescope
        self.optics = Optics(CollimationTube(first, second))
        self.reflections = Reflections(first, second, target, telescope)

        self.current_plane = None
        self.is_optics_enable = True
        self.is_reflections_enable = False

    def draw(self, plane: str) -> None:
        if plane.lower() not in ['xy', 'xz', 'yz'] or plane is None:
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

    def draw_environment(self) -> None:
        self.first.draw(self.axis, self.current_plane)
        self.second.draw(self.axis, self.current_plane)
        self.target.draw(self.axis, self.current_plane)
        self.telescope.draw(self.axis, self.current_plane)

    def draw_optics(self) -> None:
        if self.current_plane == 'xy':
            first_coeffs, second_coeffs = self.optics.get_coefficients('xy')

        if self.current_plane == 'xz':
            first_coeffs, second_coeffs = self.optics.get_coefficients('xz')

        xs = self.optics.tube.x_positions()
        ys = []

        for i in range(len(xs)):
            ys.append(first_coeffs[0] * xs[i] + first_coeffs[1])
            ys.append(second_coeffs[0] * xs[i] + second_coeffs[1]) 
        
        coordinates = [xs, ys]

        self.axis.scatter(coordinates[0], coordinates[1], color='black')

        self.axis.plot([coordinates[0][0], coordinates[0][-1]], [coordinates[1][0], coordinates[1][-1]], color='red', label='optic scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-2]], [coordinates[1][1], coordinates[1][-2]], color='red')

    def draw_reflections(self) -> None:
        if self.current_plane == 'xy':
            reflections = self.reflections.get_coefficients('xy')

        if self.current_plane == 'xz':
            reflections = self.reflections.get_coefficients('xz')

        for refl in reflections[:-1]:
            xs, ys = refl
            self.axis.plot(xs, ys, color='green')

        self.axis.plot(reflections[-1][0], reflections[-1][1], color='green', label='reflections')

    def switch_enable_optics(self) -> None:
        self.is_optics_enable = not self.is_optics_enable
        self.draw(self.current_plane)

    def switch_enable_reflections(self) -> None:
        self.is_reflections_enable = not self.is_reflections_enable
        self.draw(self.current_plane)


if __name__ == '__main__':
    pass
