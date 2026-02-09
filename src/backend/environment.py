from __future__ import annotations
import numpy
from matplotlib.axes import Axes
from matplotlib.transforms import Affine2D
from matplotlib.patches import Rectangle, Arc, Circle, Polygon


class Chamber:
    def __init__(self, diameter: float, polygon: AdditionalVolume, ctube: CollimationTube, trgt: Target, telescopes: list[Telescope]) -> None:
        self.__diameter = diameter
        self.__polygon = polygon
        self.__ctube = ctube
        self.__target = trgt
        self.__telescopes = telescopes

    @property
    def diameter(self) -> float:
        return self.__diameter
    
    @property
    def polygon(self) -> AdditionalVolume:
        return self.__polygon
    
    @property
    def target(self) -> Target:
        return self.__target
    
    @property
    def ctube(self) -> CollimationTube:
        return self.__ctube
    
    @property
    def telescopes(self) -> list[Telescope]:
        return self.__telescopes
    
    def change_ctube_length(self, new: float) -> None:
        old = self.ctube.length
        self.ctube.first_collimator.move(old - new, 0, 0)

    def move_ctube(self, new_distance: float) -> None:
        old_distance = self.target.x_position - self.ctube.second_collimator.x_position
        self.ctube.first_collimator.move(old_distance - new_distance, 0, 0)
        self.ctube.second_collimator.move(old_distance - new_distance, 0, 0)
    
    def rotate_target(self, angle: float) -> None:
        dtheta = angle - self.target.theta
        self.target.rotate(dtheta)

    def rotate_telescope(self, index: int, angle: float) -> None:
        dtheta = angle - self.telescopes[index].theta
        self.telescopes[index].rotate(dtheta)

    def draw(self, axis: Axes) -> None:
        vertices = self.polygon.separate(self.polygon.find_collisions(self.diameter))

        axis.add_patch(Circle((0.0, 0.0), self.diameter / 2, color='darkgray', label='chamber', fill=False, linewidth=2.5))
        axis.add_patch(Polygon(vertices, closed=False, color='darkgray', label='chamber', fill=False, linewidth=2.5))

        self.__target.draw(axis)
        self.__ctube.draw(axis)
        for telescope in self.__telescopes:
            telescope.draw(axis)


class AdditionalVolume:
    def __init__(self, points: list[list[float]]):
        if points[0][0] != points[-1][0] or points[0][1] != points[-1][1]:
            raise ValueError("The first and the last points must be the same!")

        points.pop()
        self.__points = points

    @property
    def points(self) -> list[float]:
        return self.__points
    
    def find_collisions(self, diameter: float) -> list[int]:
        collision_indexes = []
        for i in range(len(self.__points)):
            hypo = (self.__points[i][0] ** 2 + self.__points[i][1] ** 2) ** (1/2)

            if abs(hypo - diameter / 2) < 0.1:
                collision_indexes.append(i)

        return collision_indexes
    
    def separate(self, collision_indexes: list[int]) -> list[float]:
        transformed_points = self.__points.copy()
        while not (transformed_points[0] == self.__points[collision_indexes[0]] and transformed_points[-1] == self.__points[collision_indexes[-1]]):
            transformed_points = numpy.roll(transformed_points, shift=1, axis=0).tolist()
        
        return transformed_points


class Environment:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, theta: float = 0.0, is_clockwise: bool = True) -> None:
        self._x = x
        self._y = y
        self._z = z
        self._theta = theta
        self._is_clockwise = is_clockwise

    @property
    def x_position(self) -> float:
        return self._x
    
    @property
    def y_position(self) -> float:
        return self._y
    
    @property
    def z_position(self) -> float:
        return self._z
    
    @property
    def theta(self) -> float:
        return self._theta
    
    @property
    def is_clockwise(self) -> bool:
        return self._is_clockwise
    
    def move(self, dx: float, dy: float, dz: float) -> None:
        self._x += dx
        self._y += dy
        self._z += dz

    def rotate(self, dtheta: float) -> None:
        self._theta += dtheta
        self._theta %= 360

    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        pass


class Collimator(Environment):
    def __init__(self, diameter: float, thickness: float, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(x, y, z)
        self._d = diameter
        self._t = thickness

    @property
    def diameter(self) -> float:
        return self._d
    
    @diameter.setter
    def diameter(self, new: float) -> None:
        self._d = new
    
    @property
    def thickness(self) -> float:
        return self._t
    
    @thickness.setter
    def thickness(self, new: float) -> float:
        self._t = new
    
    @property
    def height(self) -> float:
        return 4 * self._d
    
    def draw(self, axis: Axes, plane: str = 'xy', no_rotation: bool = False, is_clockwise: bool = True) -> None:
        x1, y1, z1 = self._x, self._y, self._z
        x2, y2, z2 = self._x, self._y, self._z

        if plane == 'xy':
            theta = 360 - self._theta if is_clockwise else self._theta
            theta = 0 if no_rotation else theta

            y1 -= 0.5 * self.height 
            axis.add_patch(Rectangle(
                (x1, y1), self._t, self.height / 2 - self._d / 2, angle=theta, rotation_point=(0.0, 0.0), color='black', label='collimator'
            ))

            y2 += 0.5 * self.diameter
            axis.add_patch(Rectangle(
                (x2, y2), self._t, self.height / 2 - self._d / 2, angle=theta, rotation_point=(0.0, 0.0), color='black', label='collimator'
            ))

        if plane == 'xz':
            z1 -= 0.5 * self.height
            axis.add_patch(Rectangle(
                (x1, z1), self._t, self.height / 2 - self._d / 2, color='black', label='collimator'
            ))

            z2 += 0.5 * self.diameter
            axis.add_patch(Rectangle(
                (x2, z2), self._t, self.height / 2 - self._d / 2, color='black', label='collimator'
            ))
    

class Target(Environment):
    def __init__(self, width: float, height: float, x: float = 0.0, y: float = 0.0, z: float = 0.0, theta: float = 0.0) -> None:
        super().__init__(x, y, z, theta)
        self._w = width
        self._h = height

    @property
    def width(self) -> float:
        return self._w
    
    @width.setter
    def width(self, new: float) -> None:
        self._w = new
    
    @property
    def height(self) -> float:
        return self._h
    
    @height.setter
    def height(self, new: float) -> None:
        self._h = new

    def draw(self, axis: Axes, plane: str = "xy") -> None:
        if plane == 'xy':
            transform = Affine2D().rotate_deg(self._theta) + axis.transData
            axis.plot([self._x, self._x], [self._y - self._h / 2, self._y + self._h / 2], transform=transform, color='purple', label='target')

        if plane == 'xz':
            axis.plot([self._x, self._x], [self._z - self._h / 2, self._z + self._h / 2], color='purple', label='target')


class Detector(Environment):
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, theta: float = 0.0, is_clockwise: bool = True) -> None:
        super().__init__(x, y, z, theta, is_clockwise)

    def draw(self, axis: Axes, plane: str = 'xy', no_rotation: bool = False) -> None:
        detector_width, detector_height = 25, 25
        x, y, z = self._x, self._y, self._z

        if plane == 'xy':
            y -= 0.5 * detector_height
            theta = 360 - self._theta if self._is_clockwise else self._theta
            axis.add_patch(Rectangle(
                (x, y), 
                detector_width, 
                detector_height, 
                angle=0 if no_rotation else theta,
                rotation_point=(0.0, 0.0), 
                color="blue",
                label='detector'
            )) 

        if plane == 'xz':
            z -= 0.5 * detector_height
            axis.add_patch(Rectangle((x, z), detector_width, detector_height, color="blue", label='detector'))


class Tube(Environment):
    def __init__(self, first: Collimator, second: Collimator, theta: float = 0.0, is_clockwise: bool = True) -> None:
        x = first.x_position + first.thickness
        y = first.y_position
        z = first.z_position

        super().__init__(x, y, z, theta, is_clockwise)
        self._f = first
        self._s = second

    @property
    def first_collimator(self) -> Collimator:
        return self._f
    
    @property
    def second_collimator(self) -> Collimator:
        return self._s
    
    @property
    def length(self) -> float:
        xs = (self._s.x_position - self._f.x_position)**2
        ys = (self._s.y_position - self._f.y_position)**2
        zs = (self._s.z_position - self._f.z_position)**2
        return (xs + ys + zs) ** (1/2)
    
    def x_positions(self) -> list[float]:
        return [self._f.x_position, self._s.x_position]
    
    def y_positions(self) -> list[float]:
        return [self._f.y_position, self._s.y_position]

    def z_positions(self) -> list[float]:
        return [self._f.z_position, self._s.z_position]
    
    def move(self, dx: float, dy: float, dz: float) -> None:
        super().move(dx, dy, dz)
        self._f.move(dx, dy, dz)
        self._s.move(dx, dy, dz)
    
    def rotate(self, dtheta: float) -> None:
        super().rotate(dtheta)
        self._f.rotate(dtheta)
        self._s.rotate(dtheta)

    def draw(self, axis: Axes, plane: str = 'xy', no_rotation: bool = False) -> None:
        self._f.draw(axis, plane, no_rotation, self.is_clockwise)
        self._s.draw(axis, plane, no_rotation, self.is_clockwise)


class CollimationTube(Tube):
    def __init__(self, first: Collimator, second: Collimator) -> None:
        super().__init__(first, second)

    def draw(self, axis: Axes, plane: str = 'xy', no_rotation: bool = False) -> None:
        super().draw(axis, plane, no_rotation)


class Telescope(Tube):
    def __init__(self, first: Collimator, second: Collimator, detector: Detector) -> None:
        super().__init__(first, second, detector.theta, is_clockwise=detector.is_clockwise)
        self._detector = detector

    @property
    def detector(self) -> Detector:
        return self._detector
    
    def move(self, dx: float, dy: float, dz: float) -> None:
        super().move(dx, dy, dz)
        self._detector.move(dx, dy, dz)
    
    def rotate(self, dtheta: float) -> None:
        super().rotate(dtheta)
        self._detector.rotate(dtheta)
    
    def draw(self, axis: Axes, plane: str = 'xy', no_rotation: bool = False) -> None:
        super().draw(axis, plane, no_rotation)
        self._detector.draw(axis, plane, no_rotation)


if __name__ == '__main__':
    pass