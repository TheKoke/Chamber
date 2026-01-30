import sys

# from PyQt5.QtWidgets import QApplication
# from frontend.geomwindow import GeomWindow
# from backend.start import starting_position


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # w = GeomWindow(starting_position())
    # w.show()
    # app.exec()
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

    p = ScaledPainter(ax, geom)
    p.is_telescope_optics_enable = True
    p.draw()
    plt.show()
