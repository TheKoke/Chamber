from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, Arc


SCOPING = 10


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
    def __init__(self, radius: float, thickness: float, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(x, y, z)
        self._r = radius
        self._t = thickness
        self._h = 6 * self._r

    @property
    def radius(self) -> float:
        return self._r
    
    @radius.setter
    def radius(self, new: float) -> None:
        if new <= 0:
            return
        
        self._r = new
    
    @property
    def thickness(self) -> float:
        return self._t
    
    @thickness.setter
    def thickness(self, new: float) -> float:
        if new <= 0:
            return
        
        self._t = new
    
    @property
    def height(self) -> float:
        return self._h
    
    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        if plane == 'xy':
            axis.add_patch(Rectangle(
                (self._x, self._y + self._r / 2), self._t * SCOPING, self._h / 2 - self._r, color='black', label='collimator'
            ))

            axis.add_patch(Rectangle(
                (self._x, self._y - self._h / 2 + self._r / 2), self._t * SCOPING, self._h / 2 - self._r, color='black'
            ))

        if plane == 'xz':
            axis.add_patch(Rectangle(
                (self._x, self._z + self._r / 2), self._t * SCOPING, self._h / 2 - self._r, color='black', label='collimator'
            ))

            axis.add_patch(Rectangle(
                (self._x, self._z - self._h / 2 + self._r / 2), self._t * SCOPING, self._h / 2 - self._r, color='black'
            ))

        if plane == 'yz':
            axis.add_patch(Rectangle(
                (self._y, self._z + self._r / 2), self._t * SCOPING, self._H / 2 - self._r, color='black', label='collimator'
            ))

            axis.add_patch(Rectangle(
                (self._y, self._z - self._h / 2 + self._r / 2), self._t * SCOPING, self._h / 2 - self._r, color='black'
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
        if new <= 0:
            return
        
        self._w = new
    
    @property
    def height(self) -> float:
        return self._h
    
    @height.setter
    def height(self, new: float) -> None:
        if new <= 0:
            return
        
        self._h = new

    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        if plane == 'xy':
            axis.plot([self._x, self._x], [self._y - self._h / 2, self._y + self._h / 2], color='purple', label='target')

        if plane == 'xz':
            axis.plot([self._x, self._x], [self._z - self._h / 2, self._z + self._h / 2], color='purple', label='target')

        if plane == 'yz':
            axis.plot([self._y, self._y], [self._z - self._h / 2, self._z + self._h / 2], color='purple', label='target')


class Detector(Environment):
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(x, y, z)

    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        DETECTOR_WIDTH = 12.0
        if plane == 'xy':
            axis.add_patch(Rectangle(
                (self._x, self._y - DETECTOR_WIDTH / (2 * SCOPING)), 
                DETECTOR_WIDTH * SCOPING, 
                DETECTOR_WIDTH / SCOPING, 
                color='blue', 
                label='detector'
            ))

        if plane == 'xz':
            axis.add_patch(Rectangle(
                (self._x, self._z - DETECTOR_WIDTH / (2 * SCOPING)), 
                DETECTOR_WIDTH * SCOPING, 
                DETECTOR_WIDTH / SCOPING, 
                color='blue', 
                label='detector'
            ))

        if plane == 'yz':
            axis.add_patch(Rectangle(
                (self._y, self._z - DETECTOR_WIDTH / (2 * SCOPING)), 
                DETECTOR_WIDTH * SCOPING, 
                DETECTOR_WIDTH / SCOPING, 
                color='blue', 
                label='detector'
            ))


class Faraday(Environment):
    def __init__(self, length: float, radius: float, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        super().__init__(x, y, z)

        self._l = length
        self._r = radius

    @property
    def length(self) -> float:
        return self._l
    
    @length.setter
    def length(self, new: float) -> None:
        if new <= 0:
            return
        
        self._l = new

    @property
    def radius(self) -> float:
        return self._r
    
    @radius.setter
    def radius(self, new: float) -> None:
        if new <= 0:
            return
        
        self._r = new

    def draw(self, axis: Axes, plane: str = 'xy') -> None:
        if plane == 'xy':
            pass

        if plane == 'xz':
            pass

        if plane == 'yz':
            pass


if __name__ == '__main__':
    pass
