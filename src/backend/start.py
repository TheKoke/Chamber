from backend.geometry import Geometry
from backend.environment import Chamber, AdditionalVolume, CollimationTube, Collimator, Target, Telescope


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
    first_collimator = Collimator(3.0, 2.0, x=0.0)
    second_collimator = Collimator(3.0, 2.0, x=601.0)
    collimation = CollimationTube(first_collimator, second_collimator)

    target = Target(15.0, 15.0, x=1368.0)

    near_collimator1 = Collimator(4.9, 1.0, x=1448.0)
    near_collimator2 = Collimator(4.9, 1.0, x=1638.0)
    near_telescope = Telescope(near_collimator1, near_collimator2)

    rear_collimator1 = Collimator(3.0, 1.0, x=2068.0)
    rear_collimator2 = Collimator(3.0, 1.0, x=2318.0)
    rear_telescope = Telescope(rear_collimator1, rear_collimator2)

    points = [
        [  320.087, -90.0  ],
        [ 1040.087, -90.0  ],
        [ 1040.087,  90.0  ],
        [  815.812, 491.622],
        [  285.756,  170   ]
    ]
    back = AdditionalVolume(points)

    chamber = Chamber(665.0, back, collimation, target, [near_telescope, rear_telescope])
    return Geometry(chamber)


if __name__ == '__main__':
    pass
