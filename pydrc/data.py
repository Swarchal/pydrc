import pandas as pd
import numpy as np

from io import StringIO
import textwrap


def two_cmpds(log_x: bool = False) -> pd.DataFrame:
    data = textwrap.dedent(
        """
        conc,response,drug
        1.00E-10,0,A
        1.00E-08,1,A
        3.00E-08,12,A
        1.00E-07,19,A
        3.00E-07,28,A
        1.00E-06,32,A
        3.00E-06,35,A
        1.00E-05,39,A
        3.00E-05,,A
        1.00E-04,39,A
        3.00E-04,,A
        1.00E-10,0,A
        1.00E-08,0,A
        3.00E-08,10,A
        1.00E-07,18,A
        3.00E-07,30,A
        1.00E-06,35,A
        3.00E-06,41,A
        1.00E-05,43,A
        3.00E-05,,A
        1.00E-04,43,A
        3.00E-04,,A
        1.00E-10,0,A
        1.00E-08,4,A
        3.00E-08,15,A
        1.00E-07,22,A
        3.00E-07,28,A
        1.00E-06,35,A
        3.00E-06,38,A
        1.00E-05,44,A
        3.00E-05,,A
        1.00E-04,44,A
        3.00E-04,,A
        1.00E-10,0,B
        1.00E-08,,B
        3.00E-08,1,B
        1.00E-07,5,B
        3.00E-07,8,B
        1.00E-06,17,B
        3.00E-06,23,B
        1.00E-05,27,B
        3.00E-05,30,B
        1.00E-04,32,B
        3.00E-04,32,B
        1.00E-10,0,B
        1.00E-08,,B
        3.00E-08,0,B
        1.00E-07,3,B
        3.00E-07,10,B
        1.00E-06,20,B
        3.00E-06,38,B
        1.00E-05,31,B
        3.00E-05,34,B
        1.00E-04,37,B
        3.00E-04,37,B
        1.00E-10,0,B
        1.00E-08,,B
        3.00E-08,2,B
        1.00E-07,6,B
        3.00E-07,12,B
        1.00E-06,23,B
        3.00E-06,29,B
        1.00E-05,34,B
        3.00E-05,38,B
        1.00E-04,38,B
        3.00E-04,,B
    """
    )
    data_io = StringIO(data)
    df = pd.read_csv(data_io)
    if log_x:
        df["conc"] = np.log10(df["conc"])
    return df
