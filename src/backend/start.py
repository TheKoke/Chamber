from backend.geometry import Geometry
from backend.environment import Collimator, Detector, Target


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
    second_collimator = Collimator(3.0, 2.0, x=600.0)

    target = Target(15.0, 15.0, x=1320.0)

    detector = Detector(x=1540.0)

    geometry = Geometry([first_collimator, second_collimator], target, detector)
    return geometry

"""
from backend.environment import *
    from backend.geometry import *
    from backend.painter import *
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    points = [
        [320.087, -90.0],
        [1040.087, -90.0],
        [1040.087, 90.0], 
        [815.812, 491.622],
        [285.756, 170.0],
        [320.087, -90.0]
    ]
    f = Collimator(3.0, 2.0, x=-1368.0)
    s = Collimator(3.0, 2.0, x=-767.0)
    t_f1 = Collimator(5.5, 1.0, x=80.0)
    t_s1 = Collimator(4.0, 1.0, x=270.0)
    t_f2 = Collimator(5.5, 1.0, x=700.0)
    t_s2 = Collimator(4.0, 1.0, x=925.0)

    back = AdditionalVolume(points)
    c = CollimationTube(f, s)
    t = Target(10.0, 10.0)
    teles = [Telescope(t_f1, t_s1), Telescope(t_f2, t_s2, is_clockwise=False)]
    teles[0].rotate(20)
    teles[1].rotate(20)

    ch = Chamber(665.0, back, c, t, teles)
    geom = Geometry(ch)

    p = FullPainter(ax, geom)
    plt.show()
"""


if __name__ == '__main__':
    pass
