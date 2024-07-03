from geometry import Geometry

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle


class Painter:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

    def draw(self) -> None:
        pass


if __name__ == '__main__':
    pass
