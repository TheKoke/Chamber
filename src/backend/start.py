from geometry import Geometry
from environment import Collimator, Detector, Target


def starting_position() -> Geometry:
    '''
    Starting position function:\n
    It is the geometry of scattering chamber of \n
    Laboratory of Low-Energy Nuclear Reactions in\n
    U-150M Cyclotrone at\n
    Institute of Nuclear Physics, Almaty, Kazakhstan.

    Returns
    -------
    geometry: ``Geometry``
        geometry of LLENR scattering chamber.
    '''
    first_collimator = Collimator(3.0, 2.0)
    second_collimator = Collimator(3.0, 2.0, 960.0)

    target = Target(15.0, 15.0, 1320.0)

    detector = Detector(1540.0, 0.0, 0.0)

    geometry = Geometry(first_collimator, second_collimator, target, detector)
    return geometry


if __name__ == '__main__':
    pass
