import numpy

from backend.geometry import Geometry

from matplotlib.axes import Axes
from matplotlib.patches import Ellipse, Rectangle


class SpotModel:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

    def draw(self) -> None:
        w, h = self.calculate_width(), self.calculate_height()
        ang = self.calculate_angle()
        target = self.model.chamber.target

        self.axis.add_patch(Rectangle(
            (-target.width / 2, -target.height / 2), 
            target.width, 
            target.height, 
            color='purple', 
            label='Target'
        ))

        self.axis.add_patch(Ellipse(
            (0, 0), 
            w, h, 
            angle=ang, 
            color='red', 
            label='After beam spot'
        ))

        self.axis.set_aspect('equal')
        self.axis.set_xlim((-target.width, target.width))
        self.axis.set_ylim((-target.height, target.height))

        self.axis.grid()
        self.axis.legend()

    def calculate_angle(self) -> float:
        y1 = self.model.chamber.ctube.first_collimator.y_position
        y2 = self.model.chamber.ctube.second_collimator.y_position
        dy = y2 - y1

        z1 = self.model.chamber.ctube.first_collimator.z_position
        z2 = self.model.chamber.ctube.second_collimator.z_position
        dz = z2 - z1

        if dy == 0:
            return 90

        return 90 + numpy.rad2deg(numpy.arctan(dz / dy))

    def calculate_width(self) -> float:
        d1 = self.model.chamber.ctube.first_collimator.diameter
        d2 = self.model.chamber.ctube.second_collimator.diameter

        y1 = self.model.chamber.ctube.first_collimator.y_position
        y2 = self.model.chamber.ctube.second_collimator.y_position
        dy = abs(y2 - y1)

        z1 = self.model.chamber.ctube.first_collimator.z_position
        z2 = self.model.chamber.ctube.second_collimator.z_position
        dz = abs(z2 - z1)

        xn = self.model.spot_on_target() / self.model.chamber.ctube.second_collimator.diameter
        distance = numpy.sqrt(dy ** 2 + dz ** 2)

        return xn * (d1 + d2 - distance) / 2

    def calculate_height(self) -> float:
        d1 = self.model.chamber.ctube.first_collimator.diameter
        d2 = self.model.chamber.ctube.second_collimator.diameter

        y1 = self.model.chamber.ctube.first_collimator.y_position
        y2 = self.model.chamber.ctube.second_collimator.y_position
        dy = abs(y2 - y1)

        z1 = self.model.chamber.ctube.first_collimator.z_position
        z2 = self.model.chamber.ctube.second_collimator.z_position
        dz = abs(z2 - z1)

        distance = numpy.sqrt(dy ** 2 + dz ** 2)
        s = (d1 + d2 + distance) / 2

        xn = self.model.spot_on_target() / self.model.chamber.ctube.second_collimator.diameter

        if distance == 0:
            return xn * (d1 + d2 - distance) / 2
        
        return 2 * xn * numpy.sqrt(s * (s - d1) * (s - d2) * (s - distance)) / distance


if __name__ == '__main__':
    pass
