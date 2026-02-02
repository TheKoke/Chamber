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

        self.model.chamber.draw(self.axis)

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
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

        self.current_plane = None
        self.is_optics_enable = True
        self.is_reflections_enable = False
        self.draw()

    def draw(self, plane: str = 'xy') -> None:
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

        self.axis.set_title(f'{self.current_plane.upper()} View of Chamber')
        handles, labels = self.clear_labels()
        self.axis.legend(handles, labels)
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
        self.model.chamber.ctube.draw(self.axis, self.current_plane, no_rotation=True)
        self.model.chamber.target.draw(self.axis, self.current_plane)
        self.model.chamber.telescopes[0].draw(self.axis, self.current_plane, no_rotation=True)

    def draw_optics(self) -> None:
        coordinates = self.model.collimator_optics(self.current_plane)

        self.axis.scatter(coordinates[0], coordinates[1], color='black')

        self.axis.plot([coordinates[0][0], coordinates[0][-2]], [coordinates[1][0], coordinates[1][-2]], color='red', label='optic scatter')
        self.axis.plot([coordinates[0][1], coordinates[0][-1]], [coordinates[1][1], coordinates[1][-1]], color='red')

    def draw_reflections(self) -> None:
        reflections = self.model.collimator_reflections(self.current_plane)
        for refl in reflections:
            self.axis.plot(refl[0], refl[1], color='green', label='reflections')

    def switch_optics(self) -> None:
        self.is_optics_enable = not self.is_optics_enable
        self.draw(self.current_plane)

    def switch_reflections(self) -> None:
        self.is_reflections_enable = not self.is_reflections_enable
        self.draw(self.current_plane)


if __name__ == '__main__':
    pass
