from ninmpl import FigureBase, AxesBase
from matplotlib import pyplot as plt
import numpy as np


def test():
    class PlotAngle(AxesBase):
        options = dict(projection='polar')

        def adjust(self):
            self.ax.set_title('Circle')

    class PlotLine(AxesBase):
        def plot(self, x, name):
            self.ax.plot(x)
            self.ax.set_title(name)

    class NinFigure(FigureBase):
        def adjust(self):
            self.fig.set_figwidth(5)
            self.fig.set_figheight(5)
            self.gridspec = plt.GridSpec(2, 4, hspace=0.4)
            self.gridspec.set_height_ratios([1, 2])

    r = np.arange(0, 2, 0.01)
    theta = 2 * np.pi * r
    line = [[1, 2], [2, 1]]
    line2 = [[1, 1], [3, 4]]
    line2 = [[1, 1], [3, 4], [8, 9]]

    with NinFigure() as nf:
        nf[0, 0] = PlotAngle(r, theta)
        nf[1, 0] = PlotLine(line, 'Line')
        nf[0, 1:3] = PlotLine(line2, 'Line2')
        nf[1, 1:2] = PlotLine(line2, 'Line3')
        print(nf[1, 0].get_status())
        nf[1, 2: 4] = PlotAngle(r, theta)
        print(nf.used)

    with NinFigure() as nf:
        nf[0, 0] = PlotAngle(r, theta)
        nf[0, 0] = PlotLine(line, 'Line')


if __name__ == '__main__':
    test()
    from itertools import product
