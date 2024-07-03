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


class Collimator(Environment):
    def __init__(self, radius: float, thickness: float, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(x, y, z)
        self._r = radius
        self._t = thickness

    @property
    def radius(self) -> float:
        return self._r
    
    @property
    def thickness(self) -> float:
        return self._t
    

class Target(Environment):
    def __init__(self, width: float, height: float, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(x, y, z)
        self._w = width
        self._h = height

    @property
    def width(self) -> float:
        return self._w
    
    @property
    def height(self) -> float:
        return self._h


class Detector(Environment):
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(x, y, z)


if __name__ == '__main__':
    pass
