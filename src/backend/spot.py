from geometry import Geometry

from matplotlib.axes import Axes
from matplotlib.patches import Ellipse


class SpotModel:
    def __init__(self, axis: Axes, model: Geometry) -> None:
        self.axis = axis
        self.model = model

    def draw() -> None:
        pass


if __name__ == '__main__':
    pass
