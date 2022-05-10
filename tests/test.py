import pandas as pd
import numpy as np
from pydrc import DRC3
from pydrc import data
import matplotlib.pyplot as plt


df = data.test_data1()
df = df.dropna()

drc = DRC3()

drc.fit_plot(df.conc, df.response, df.drug)
print(drc.model_store)
