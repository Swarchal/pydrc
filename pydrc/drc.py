"""
Actual dose response fitting classes.
"""

from typing import Optional, NamedTuple, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from .mytypes import ArrayLike


class Params3(NamedTuple):
    top: float
    bottom: float
    ec50: float


class DataStats(NamedTuple):
    min_x: float
    max_x: float


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
        self.model_store = None
        self.param_store = None

    @staticmethod
    def model():
        raise NotImplementedError

    def _fit(self, x, y, c=None):
        raise NotImplementedError

    def fit(self, x: ArrayLike, y: ArrayLike, c: Optional[ArrayLike] = None):
        param_store = {}
        data_store = {}
        if c is not None:
            df = pd.DataFrame({"x": x, "y": y, "c": c})
            for name, group in df.groupby("c"):
                params, datastat = self._fit(group.x, group.y, group.c)
                param_store[name] = params
                data_store[name] = datastat
            self.param_store = param_store
            self.data_store = data_store
        else:
            params, datastats = self._fit(x, y)
            self.param_store = params
            self.data_store = datastats

    def fit_plot(self, x, y, c=None):
        self.fit(x, y, c)
        if c is not None:
            df = pd.DataFrame({"x": x, "y": y, "c": c})
            for name, group in df.groupby("c"):
                plt.scatter(group.x, group.y, label=name)
            plt.xscale("log")
            for i in self.model_store.keys():
                xmin, xmax = self.data_store[i]
                x = np.logspace(np.log10(xmin), np.log10(xmax), 1000)
                y = self.model(x, *self.model_store[i])
                plt.plot(x, y, label=i)
            plt.legend()
            plt.show()
        else:
            plt.scatter(x, y)
            plt.xscale("log")
            xmin, xmax = self.data_store
            x = np.logspace(np.log10(xmin), np.log10(xmax), 1000)
            y = self.model(x, *self.model_store)
            plt.plot(x, y)
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
    ) -> Tuple[Params3, DataStats]:
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
        min_x, max_x = min(x), max(x)
        return Params3(top, bottom, ec50), DataStats(min_x, max_x)


class DRC4(BaseDRC):
    """4 parameter dose response curve"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError("not made this yet")
