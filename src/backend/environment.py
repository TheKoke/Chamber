class Collimator:
    def __init__(self, radius: float, thickness: float, x: float = 0.0, y: float = 0.0) -> None:
        self._r = radius
        self._t = thickness
        self._x = x
        self._y = y

    @property
    def radius(self) -> float:
        return self._r
    
    @property
    def thickness(self) -> float:
        return self._t
    
    @property
    def x_position(self) -> float:
        return self._x
    
    @property
    def y_position(self) -> float:
        return self._y
    

class Target:
    def __init__(self, width: float, height: float, x: float = 0.0, y: float = 0.0) -> None:
        self._w = width
        self._h = height
        self._x = x
        self._y = y

    @property
    def width(self) -> float:
        return self._w
    
    @property
    def height(self) -> float:
        return self._h
    
    @property
    def x_position(self) -> float:
        return self._x
    
    @property
    def y_position(self) -> float:
        return self._y


class Detector:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._x = x
        self._y = y

    @property
    def x_position(self) -> float:
        return self._x
    
    @property
    def y_position(self) -> float:
        return self._y


if __name__ == '__main__':
    pass
