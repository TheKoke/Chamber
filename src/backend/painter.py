from matplotlib.axes import Axes
from matplotlib.transforms import Affine2D
from backend.geometry import Geometry, Optics, Reflections
from backend.environment import Collimator, Target, Telescope, CollimationTube


class ScaledPainter:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

        self.is_collimator_optics_enable = False
        self.is_telescope_optics_enable = False
        self.is_labels_enable = False

        self.draw()

    def draw(self) -> None:
        self.axis.clear()

        self.draw_environment()

        xmin, xmax = self.axis.get_xlim()
        self.axis.plot([xmin, xmax], [0, 0], '--', color='red', label='beam line')

        if self.is_collimator_optics_enable:
            self.draw_collimator_optics()

        if self.is_telescope_optics_enable:
            self.draw_telescope_optics()

        handles, labels = self.clear_labels()
        if self.is_labels_enable: self.axis.legend(handles, labels)
        self.axis.set_title(f'Full View of Chamber')
        self.axis.set_aspect('equal')
        self.axis.grid()

    def clear_labels(self) -> tuple[list, list]:
        handles, labels = self.axis.get_legend_handles_labels()

        dups = []
        for i in range(len(labels)):
            if i in dups: continue
            for j in range(len(labels)):
                if i == j: continue
                if labels[i] == labels[j]: dups.append(j)
        
        new_handles, new_labels = [], []
        for i in range(len(labels)):
            if i in dups: continue
            new_handles.append(handles[i])
            new_labels.append(labels[i])

        return new_handles, new_labels

    def draw_environment(self) -> None:
        self.model.chamber.draw(self.axis)
        self.model.chamber.ctube.draw(self.axis, 'xy')
        self.model.chamber.target.draw(self.axis, 'xy')
        
        for t in self.model.chamber.telescopes:
            t.draw(self.axis, 'xy')

    def draw_collimator_optics(self) -> None:
        coordinates = self.model.collimator_optics()

        self.axis.scatter(coordinates[0], coordinates[1], color='black')
        
        self.axis.plot([coordinates[0][0], coordinates[0][-2]], [coordinates[1][0], coordinates[1][-2]], color='red', label='collim. scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-1]], [coordinates[1][1], coordinates[1][-1]], color='red')

    def draw_telescope_optics(self) -> None:
        coordinates = self.model.telescope_optics()
        
        for i in range(len(self.model.chamber.telescopes)):
            angle = self.model.chamber.telescopes[i].theta
            transform = Affine2D().rotate_deg(angle) + self.axis.transData

            self.axis.scatter(coordinates[i][0], coordinates[i][1], transform=transform, color='blue')
            
            self.axis.plot([coordinates[i][0][0], coordinates[i][0][-2]], [coordinates[i][1][0], coordinates[i][1][-2]], transform=transform, color='blue', label='telesc. scatter')
            self.axis.plot([coordinates[i][0][1], coordinates[i][0][-1]], [coordinates[i][1][1], coordinates[i][1][-1]], transform=transform, color='blue')

    def switch_collimator_optics(self) -> None:
        self.is_collimator_optics_enable = not self.is_collimator_optics_enable
        self.draw()

    def switch_telescope_optics(self) -> None:
        self.is_telescope_optics_enable = not self.is_telescope_optics_enable
        self.draw()

    def switch_labels(self) -> None:
        self.is_labels_enable = not self.is_labels_enable
        self.draw()

    def add_pointer(self, x: float) -> None:
        pass


class UnscaledPainter:
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
