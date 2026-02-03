from backend.geometry import Geometry
from backend.environment import Chamber, AdditionalVolume, CollimationTube, Collimator, Target, Telescope, Detector


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
    first_collimator = Collimator(3.0, 2.0, x=-1368.0)
    second_collimator = Collimator(3.0, 2.0, x=-767.0)
    collimation = CollimationTube(first_collimator, second_collimator)

    target = Target(15.0, 15.0, x=0.0)

    near_collimator11 = Collimator(4.9, 1.0, x=80.0)
    near_collimator12 = Collimator(4.9, 1.0, x=270.0)
    near_detector1 = Detector(x=near_collimator12.x_position+near_collimator12.thickness)
    near_telescope1 = Telescope(near_collimator11, near_collimator12, near_detector1)

    near_collimator21 = Collimator(4.9, 1.0, x=80.0)
    near_collimator22 = Collimator(4.9, 1.0, x=270.0)
    near_detector2 = Detector(x=near_collimator22.x_position+near_collimator22.thickness, is_clockwise=False)
    near_telescope2 = Telescope(near_collimator21, near_collimator22, near_detector2)

    rear_collimator1 = Collimator(3.0, 1.0, x=700.0)
    rear_collimator2 = Collimator(3.0, 1.0, x=900.0)
    rear_detector = Detector(x=rear_collimator2.x_position+rear_collimator2.thickness, is_clockwise=False)
    rear_telescope = Telescope(rear_collimator1, rear_collimator2, rear_detector)

    points = [
        [  320.087, -90.0  ],
        [ 1040.087, -90.0  ],
        [ 1040.087,  90.0  ],
        [  815.812, 491.622],
        [  285.756, 170.   ],
        [  320.087, -90.0  ]
    ]
    back = AdditionalVolume(points)

    near_telescope1.rotate(20)
    near_telescope2.rotate(20)
    rear_telescope.rotate(20)

    chamber = Chamber(665.0, back, collimation, target, [near_telescope1, near_telescope2, rear_telescope])
    return Geometry(chamber)


if __name__ == '__main__':
    pass
