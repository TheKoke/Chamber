from __future__ import annotations
import numpy
from matplotlib.axes import Axes
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

    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        vertices = self.polygon.separate(self.polygon.points, self.polygon.find_collisions(self.diameter))

        axis.add_patch(Circle((0.0, 0.0), self.diameter / 2, color='darkgray', label='chamber'))
        axis.add_patch(Polygon(vertices, closed=False, color='darkgray'))


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

            if abs(hypo - diameter) < 0.1:
                collision_indexes.append(i)

        return collision_indexes
    
    def separate(self, points: list[float], collision_indexes: list[int]) -> list[float]:
        transformed_points = points.copy()
        while transformed_points[0] == points[collision_indexes[0]] and transformed_points[-1] == points[collision_indexes[-1]]:
            transformed_points = list(numpy.roll(transformed_points, shift=1))
        
        return transformed_points


class Tube:
    def __init__(self, first: Collimator, second: Collimator, theta: float = 0.0) -> None:
        self._f = first
        self._s = second
        self._theta = theta

    @property
    def first_collimator(self) -> Collimator:
        return self._f
    
    @property
    def second_collimator(self) -> Collimator:
        return self._s
    
    @property
    def theta(self) -> float:
        return self._theta
    
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
    
    def rotate(self, dtheta: float) -> None:
        if (self._theta + dtheta) < 0 or (self._theta + dtheta) > 180:
            return

        self._theta += dtheta

        for c in [self._f, self._s]:
            dx = c.x_position * (numpy.cos(numpy.radians(self._theta)) - 1) - c.y_position * numpy.sin(numpy.radians(self._theta))
            dy = c.x_position * numpy.sin(numpy.radians(self._theta)) + c.y_position * (numpy.cos(numpy.radians(self._theta)) - 1)
            dz = 0

            c.move(dx, dy, dz)

    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        self._f.draw(axis, plane)
        self._s.draw(axis, plane)


class CollimationTube(Tube):
    def __init__(self, first: Collimator, second: Collimator) -> None:
        super().__init__(first, second)

    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        super().draw(axis, plane)


class Telescope(Tube):
    def __init__(self, first: Collimator, second: Collimator) -> None:
        super().__init__(first, second)
    
    @property
    def detector_position(self) -> tuple[float, float, float]:
        return (self._s.x_position, self._s.y_position, self._s.z_position)
    
    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        super().draw(axis, plane)
        
        detector_width, detector_height = 50, 50
        detector_x, detector_y, detector_z = self.detector_position

        if plane == 'xy':
            detector_x -= numpy.sin(numpy.radians(self._theta)) * (self._s.thickness + 0.5 * detector_height)
            detector_y += numpy.cos(numpy.radians(self._theta)) * (self._s.thickness + 0.5 * detector_height)
            axis.add_patch(Rectangle((detector_x, detector_y), detector_width, detector_height, angle=360-self._theta, rotation_point=(0.0, 0.0), color="blue", label='detector'))

        if plane == 'xz':
            detector_x += self._s.thickness
            detector_z -= 0.5 * detector_height
            axis.add_patch(Rectangle((detector_x, detector_z), detector_width, detector_height, color="blue", label='detector'))


class Environment:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self._x = x
        self._y = y
        self._z = z

    @property
    def x_position(self) -> float:
        return self._x
    
    @property
    def y_position(self) -> float:
        return self._y
    
    @property
    def z_position(self) -> float:
        return self._z
    
    def move(self, dx: float, dy: float, dz: float) -> None:
        self._x += dx
        self._y += dy
        self._z += dz

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
        return 6 * self._d
    
    def draw(self, axis: Axes, plane: str = 'xy', theta: float = 0.0) -> None:
        x1, y1, z1 = self._x, self._y, self._z
        x2, y2, z2 = self._x, self._y, self._z

        if plane == 'xy':
            x1 -= 0.5 * self.height * numpy.sin(numpy.radians(theta))
            y1 += 0.5 * self.height * numpy.cos(numpy.radians(theta)) 
            axis.add_patch(Rectangle(
                (x1, y1), self._t, self.height / 2 - self._d / 2, color='black', label='collimator'
            ))

            axis.add_patch(Rectangle(
                (x2, y2), self._t, self.height / 2 - self._d / 2, color='black'
            ))

        if plane == 'xz':
            axis.add_patch(Rectangle(
                (x1, z1), self._t, self.height / 2 - self._d, color='black'
            ))

            axis.add_patch(Rectangle(
                (x2, z2), self._t, self.height / 2 - self._d, color='black'
            ))
    

class Target(Environment):
    def __init__(self, width: float, height: float, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(x, y, z)
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
            axis.plot([self._x, self._x], [self._y - self._h / 2, self._y + self._h / 2], color='purple', label='target')

        if plane == 'xz':
            axis.plot([self._x, self._x], [self._z - self._h / 2, self._z + self._h / 2], color='purple', label='target')


if __name__ == '__main__':
    pass