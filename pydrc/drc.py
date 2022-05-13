"""
Actual dose response fitting classes.
"""

from typing import Optional, NamedTuple, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from .mytypes import ArrayLike


class Params(NamedTuple):
    top: float
    bottom: float
    ec50: float
    hillslope: Optional[float] = 1.0


class BaseDRC:
    def __init__(
        self,
        iter: int = 500,
        init: Optional[ArrayLike] = None,
        bounds: Optional[ArrayLike] = None,
        rescale: bool = False,
    ):
        self.x = None
        self.y = None
        self.c = None
        self.rescale = rescale
        self.method = "trf"
        self.iter = iter
        self.init = init
        self.bounds = bounds
        self.param_store = None

    @staticmethod
    def model(*args):
        raise NotImplementedError

    def _fit(self, x: ArrayLike, y: ArrayLike, c: Optional[ArrayLike] = None) -> Params:
        popt, *_ = curve_fit(
            self.model,
            x,
            y,
            p0=self.init,
            method=self.method,
            bounds=self.bounds,
            maxfev=self.iter,
        )
        return Params(*popt)

    def do_rescaling(self, y: ArrayLike, c: Optional[ArrayLike] = None) -> ArrayLike:
        """rescale each response between 0 and 100"""
        y = np.asarray(y)

        def _rescale_group(df: pd.DataFrame) -> pd.DataFrame:
            ymin = df.y.min()
            ymax = df.y.max()
            df.y = (df.y - ymin) / (ymax - ymin) * 100
            return df

        if c is not None:
            df = pd.DataFrame({"y": y, "c": c})
            df = df.groupby("c").apply(_rescale_group)
            return df.y.values
        return (y - y.min()) / (y.max() - y.min()) * 100

    def fit(self, x: ArrayLike, y: ArrayLike, c: Optional[ArrayLike] = None):
        if self.rescale:
            y = self.do_rescaling(y, c)
        self.x, self.y, self.c = x, y, c
        param_store = {}
        if c is not None:
            df = pd.DataFrame({"x": x, "y": y, "c": c})
            for name, group in df.groupby("c"):
                param_store[name] = self._fit(group.x, group.y, group.c)
            self.param_store = param_store
        else:
            self.param_store = self._fit(x, y)

    def plot(self, xscale="log"):
        assert self.x is not None and self.y is not None
        assert self.param_store is not None
        xmin, xmax = min(self.x), max(self.x)
        x_interp = np.logspace(np.log10(xmin), np.log10(xmax), 1000)
        if self.c is not None:
            df = pd.DataFrame({"x": self.x, "y": self.y, "c": self.c})
            for name, group in df.groupby("c"):
                plt.scatter(group.x, group.y, label=name)
            plt.xscale(xscale)
            for i in self.param_store.keys():
                y_interp = self.model(x_interp, *self.param_store[i])
                plt.plot(x_interp, y_interp, label=i)
            plt.legend()
            plt.show()
        else:
            plt.scatter(self.x, self.y)
            plt.xscale(xscale)
            y_interp = self.model(x_interp, *self.param_store)
            plt.plot(x_interp, y_interp)
            plt.show()


class DRC3(BaseDRC):
    """3 parameter dose response curve"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.bounds is None:
            self.bounds = ((-np.inf, -np.inf, -np.inf), (np.inf, np.inf, np.inf))

    @staticmethod
    def model(x, top, bottom, ec50, hillslope=1) -> np.ndarray:
        return bottom + x * (top - bottom) / (ec50 + x)


class DRC4(BaseDRC):
    """4 parameter dose response curve"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.init is None:
            self.init = (100, 0, 0.1, 1)
        if self.bounds is None:
            self.bounds = ((-np.inf, -np.inf, -np.inf, -3), (np.inf, np.inf, np.inf, 3))

    @staticmethod
    def model(x, top, bottom, ec50, hillslope) -> np.ndarray:
        return bottom + (x ** hillslope) * (top - bottom) / (
            (x ** hillslope) + (ec50 ** 1)
        )
