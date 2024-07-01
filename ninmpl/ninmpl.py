""" ninplot
Simple matplotlib context manager package.
It based on OOP, especially inheritance.

>>> from ninplot import FigureBase, AxesBase
>>> class PlotAngle(AxesBase):
>>>     options = dict(projection='polar')
>>>
>>>     def adjust(self):
>>>         self.ax.set_title('Circle')
>>>
>>> class PlotLine(AxesBase):
>>>     def adjust(self):
>>>         self.ax.set_title('Line')
>>>
>>> class NinFigure(FigureBase):
>>>     def adjust(self):
>>>         self.fig.set_figwidth(5)
>>>         self.fig.set_figheight(5)
>>>         self.gridspec = plt.GridSpec(2, 4, hspace=0.4)
>>>         self.gridspec.set_height_ratios([1, 2])
>>>
>>> r = np.arange(0, 2, 0.01)
>>> theta = 2 * np.pi * r
>>> line = [[1, 2], [2, 1]]
>>> line2 = [[1, 1], [3, 4]]
>>>
>>> with NinFigure() as nf:
>>>     nf[0, 0] = PlotAngle(r, theta)
>>>     nf[1, 0] = PlotLine(line)
>>>     nf[0, 1:3] = PlotLine(line2)
>>>     print(nf[1, 0].get_status())
"""

from typing import Optional
import abc
import itertools
from matplotlib import pyplot as plt


class SamePlaceException(Exception):
    pass

def range_as_int(x) -> tuple[int, int]:
    if isinstance(x, int):
        return (x, x + 1)
    elif isinstance(x, slice):
        return (x.start, x.stop)
    else:
        raise TypeError('Not int or slice')

def get_points(y, x):
    return itertools.product(range())


class AxesBase:
    """
    Base class to use axes.
    AxesBase.adjust method adjusts axes.
    AxesBase.plot method draws figure.
    You should inherit it and use with FigureBase.

    Arguments
    ----------
    *args: Any
        Arguments to plot.
    **kwargs: Any
        Keyword arguments to plot.

    >>> class PlotAngle(AxesBase):
    >>>     options = dict(projection='polar')
    >>>     def adjust(self):
    >>>         self.ax.set_title('Circle')
    >>>     def plot(self, x, y):
    >>>         self.ax.plot(x, y)
    """
    options = {}

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def make_ax(self, fig: plt.Figure, subplotspec: plt.SubplotSpec):
        """
        Make axes from plt.Figure and plt.SubplotSpec.
        If you want to use some special Axes like 'polar axes',
        please override AxesBase.options.

        Arguments
        ----------
        fig: matplotlib.pyplot.Figure
            Figure object to use.
        subplotspec: matplotlib.pyplot.SubplotSpec
            Part of GridSpec object.
        """
        self.ax: plt.Axes = fig.add_subplot(
            subplotspec, **self.options)
        return self

    @abc.abstractmethod
    def adjust(self):
        """
        Please override this method to adjust plots.
        """
        pass

    def _plot(self):
        im = self.plot(*self.args, **self.kwargs)
        self.adjust()
        return im

    @abc.abstractmethod
    def plot(self, *args, **kwargs):
        """
        Please override this method to plot.
        """
        return self.ax.plot(*args, **kwargs)

    def get_status(self) -> plt.SubplotSpec:
        """
        Get subplotspec object of axes.
        Using this, you can know the location of an axes.
        """
        return self.ax.get_subplotspec()


class FigureBase:
    """
    Class to use matplotlib in context manager.
    It plot or save figure automatically.
    Please inherit it and override adjust method
    and set self.gridspec variable in it.

    Arguments
    ----------
    gridspec: plt.GridSpec
        GridSpec object of matplotlib.
    show: bool
        Show figure or not.
    filename: Optional[str]
        If it is not None, file will be saved.

    >>> class NinFigure(FigureBase):
    >>>     def adjust(self):
    >>>         self.fig.set_figwidth(5)
    >>>         self.fig.set_figheight(5)
    >>>         self.gridspec = plt.GridSpec(2, 4, hspace=0.4)
    >>>         self.gridspec.set_height_ratios([1, 2])
    """

    def __init__(self, show=True, filename: Optional[str] = None):
        self.fig = plt.figure()
        self.show = show
        self.filename = filename
        self.plots = {}
        self.adjust()
        self.used = set()

    @abc.abstractmethod
    def adjust(self):
        """
        Please set self.gridspec.
        """
        self.gridspec = plt.GridSpec(1, 1)

    def __getitem__(self, place) -> AxesBase:
        return self.plots[*(range_as_int(x) for x in place)]

    def __setitem__(self, place, obj: AxesBase):
        all_used = itertools.product(*(range(*range_as_int(x)) for x in place))
        for used in all_used:
            if used in self.used:
                raise SamePlaceException(f'The place already used: {used}')
            self.used.add(used)
        self.plots[*(range_as_int(x) for x in place)] =\
            obj.make_ax(self.fig, self.gridspec[*place])

    def __enter__(self):
        return self

    def __exit__(self, i: any, j: any, k: any) -> None:
        if i:
            raise i(j)
        for ax in self.plots.values():
            ax._plot()
        if self.show:
            plt.show()
        if self.filename is not None:
            self.fig.savefig(self.filename)
        self.fig.clear()
