from geometry import Geometry

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, Ellipse


class Painter:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model


if __name__ == '__main__':
    pass
