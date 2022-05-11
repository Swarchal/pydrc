"""
Actual dose response fitting classes.
"""

from typing import Optional, NamedTuple

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from .mytypes import ArrayLike


class Params3(NamedTuple):
    top: float
    bottom: float
    ec50: float


class BaseDRC:
    def __init__(
        self,
        iter: int = 500,
        init: Optional[ArrayLike] = None,
        bounds: Optional[ArrayLike] = None,
    ):
        self.x = None
        self.y = None
        self.c = None
        self.method = "trf"
        self.iter = iter
        self.init = init
        self.bounds = bounds if bounds else (-np.inf, np.inf)
        self.hillslope_ = None
        self.ec50_ = None
        self.bottom_ = None
        self.top_ = None
        self.param_store = None

    @staticmethod
    def model(*args):
        raise NotImplementedError

    def _fit(self, x, y, c=None):
        raise NotImplementedError

    def fit(self, x: ArrayLike, y: ArrayLike, c: Optional[ArrayLike] = None):
        self.x, self.y, self.c = x, y, c
        param_store = {}
        if c is not None:
            df = pd.DataFrame({"x": x, "y": y, "c": c})
            for name, group in df.groupby("c"):
                param_store[name] = self._fit(group.x, group.y, group.c)
            self.param_store = param_store
        else:
            self.param_store = self._fit(x, y)

    def plot(self):
        assert self.x is not None and self.y is not None
        assert self.param_store is not None
        xmin, xmax = min(self.x), max(self.x)
        x_interp = np.logspace(np.log10(xmin), np.log10(xmax), 1000)
        if self.c is not None:
            df = pd.DataFrame({"x": self.x, "y": self.y, "c": self.c})
            for name, group in df.groupby("c"):
                plt.scatter(group.x, group.y, label=name)
            plt.xscale("log")
            for i in self.param_store.keys():
                y_interp = self.model(x_interp, *self.param_store[i])
                plt.plot(x_interp, y_interp, label=i)
            plt.legend()
            plt.show()
        else:
            plt.scatter(self.x, self.y)
            plt.xscale("log")
            y_interp = self.model(x_interp, *self.param_store)
            plt.plot(x_interp, y_interp)
            plt.show()


class DRC3(BaseDRC):
    """3 parameter dose response curve"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def model(x, top, bottom, ec50) -> np.ndarray:
        return bottom + x * (top - bottom) / (ec50 + x)

    def _fit(
        self, x: ArrayLike, y: ArrayLike, c: Optional[ArrayLike] = None
    ) -> Params3:
        popt, *_ = curve_fit(
            self.model,
            x,
            y,
            p0=self.init,
            method=self.method,
            bounds=self.bounds,
            maxfev=self.iter,
        )
        top, bottom, ec50 = popt
        return Params3(top, bottom, ec50)


class DRC4(BaseDRC):
    """4 parameter dose response curve"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError("not made this yet")
