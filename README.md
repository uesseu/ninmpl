# NinMPL
Matplotlib wrapper for me!

# Why ninmpl?
Matplotlib is based on OOP. However, I cannnot inherit objects easily.
Is it because my programming skill? I do not know but I wanted easy way to perform OOP.
This package wraps matplotlib and force user inheritance as UI.

# Usage
1. import AxesBase and FigureBase from ninmpl.
2. Inherit AxesBase and make 'adjust' and 'plot' method.
3. Inherit FigureBase and make 'adjust' method.
4. Write with statement of 3 and set gridspec.
5. Set 2 into 4.

AxesBase has 'ax' attribute and FigureBase has 'fig' attribute.
User must use them. Please read Example.

# Classes
## AxesBase
Base class to use axes.
It has 'ax' attribute and user must use it.
AxesBase.adjust method adjusts axes.
AxesBase.plot method draws figure.
You should inherit it and use with FigureBase.

```python
# Arguments
# ----------
# *args: Any
#     Arguments to plot.
# **kwargs: Any
#     Keyword arguments to plot.

>>> class PlotAngle(AxesBase):
>>>     options = dict(projection='polar')
>>>     def adjust(self):
>>>         self.ax.set_title('Circle')
>>>     def plot(self, x, y):
>>>         self.ax.plot(x, y)
```

It also has 'make_ax' method. You can use it and make axes.
If you want to use some special Axes like 'polar axes',
please override AxesBase.options.

```python
def make_ax(self, fig: plt.Figure, subplotspec: plt.SubplotSpec):
    """
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
```

## FigureBase:
Class to use matplotlib in context manager.
It plot or save figure automatically.
It has 'fig' attribute and user must use it.
Please inherit it and override adjust method
and set self.gridspec variable in it.

```python
# Arguments
# ----------
# gridspec: plt.GridSpec
#     GridSpec object of matplotlib.
# show: bool
#     Show figure or not.
# filename: Optional[str]
#     If it is not None, file will be saved.
# gridspec: Optional[matplotlib.pyplot.GridSpec]
#     GridSpec to use.
#     Default is a GridSpec to make 1 axes.

>>> class NinFigure(FigureBase):
>>>     def adjust(self):
>>>         self.fig.set_figwidth(5)
>>>         self.fig.set_figheight(5)
```

# Example
```python
from ninmpl import FigureBase, AxesBase
from matplotlib import pyplot as plt
import numpy as np


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
        self.gridspec.set_height_ratios([1, 2])

r = np.arange(0, 2, 0.01)
theta = 2 * np.pi * r
line = [[1, 2], [2, 1]]
line2 = [[1, 1], [3, 4]]
line2 = [[1, 1], [3, 4], [8, 9]]

gridspec = plt.GridSpec(2, 4, hspace=0.4)
with NinFigure(gridspec=gridspec) as nf:
    nf[0, 0] = PlotAngle(r, theta)
    nf[1, 0] = PlotLine(line, 'Line')
    nf[0, 1:3] = PlotLine(line2, 'Line2')
    nf[1, 1:2] = PlotLine(line2, 'Line3')
    print(nf[1, 0].get_status())
    nf[1, 2: 4] = PlotAngle(r, theta)
    print(nf.used)
```
