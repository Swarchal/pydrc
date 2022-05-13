# pyDRC

Dose response curve fitting in python.

Still a work in progress.

## Package aims:

- Simple scikit-learn like API.
- Easy to use with pandas DataFrames or numpy arrays.
- Sensible default parameters, but ability to tweak everything if needed.
- Easily extendable if customisation is required.
- Similar results to GraphPad Prism or R's drc package on the same datasets.


## examples


Single compound 3-param model.


```python
import pydrc

df = (
    pydrc.data.two_cmpds()
    .dropna()
    .query("drug == 'A'")
)
print(df.head())
```

```
        conc  response drug
1.000000e-10       0.0    A
1.000000e-08       1.0    A
3.000000e-08      12.0    A
1.000000e-07      19.0    A
3.000000e-07      28.0    A
```

```python
drc = pydrc.DRC3()
drc.fit(x=df_a.conc, y=df_a.response)

print(drc.param_store)
```

```
Params(
    top=40.50445968423368,
    bottom=0.3224712712407177,
    ec50=1.1004776487262973e-07,
    hillslope=1.0
)
```

------------


Multi compound 3-param model.


```python
import pydrc

df = pydrc.data.two_cmpds().dropna()

drc = pydrc.DRC3()
drc.fit(x=df.conc, y=df.response, c=df.drug)
drc.plot()
```

![pydrc_3param](https://user-images.githubusercontent.com/10051679/168306046-e99a3b7f-8a3c-4579-930a-8e5e0b1a5a7c.png)

```python
print(drc.param_store)
```

```
{
    'A': Params(top=40.5, bottom=0.3, ec50=1.1e-07, hillslope=1.0),
    'B': Params(top=34.8, bottom=-0.1, ec50=6.9e-07, hillslope=1.0)
}
```

-----------

Multi compounds 4-parameter model specifying parameter bounds.

```python
import pydrc

df = pydrc.data.two_cmpds().dropna()

# top, bottom, ec50, hillslope
mins = (0, 0, 0, -3)
maxs = (100, 100, 1, 3)

drc = pydrc.DRC4(bounds=(mins, maxs))

drc.fit(df.conc, df.response, df.drug)
drc.plot()
```

![pydrc_4param](https://user-images.githubusercontent.com/10051679/168300651-71e56d06-4c2f-43c2-a880-df13082fcbe4.png)

```python
print(drc.param_store)
```

```
{
    'A': Params(top=41.9, bottom=2.3, ec50=2.9e-06, hillslope=0.8),
    'B': Params(top=34.7, bottom=8.9e-16, ec50=4.7e-07, hillslope=1.0)
}
```

------------

Multi compounds, parameter bounds and rescaling values to min-max.

```python
import pydrc

df = pydrc.data.two_cmpds().dropna()

# top, bottom, ec50, hillslope
mins = (0, 0, 0, -3)
maxs = (100, 100, 1, 3)

drc = pydrc.DRC4(rescale=True, bounds=(mins, maxs))

drc.fit(df.conc, df.response, df.drug)
drc.plot()
```

![pydrc_4param_rescaled](https://user-images.githubusercontent.com/10051679/168308427-8d8a1387-1b69-4cd6-832c-65e62ab19462.png)


```python
print(drc.param_store)
```

```
{
    'A': Params(top=95.3, bottom=4.7e-13, ec50=2.9e-06, hillslope=0.80),
    'B': Params(top=91.5, bottom=9.8e-14, ec50=4.7e-07, hillslope=1.0)
}
```

