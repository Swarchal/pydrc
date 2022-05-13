# pyDRC

Dose response curve fitting in python.


## examples


Single compound 3-param model.


```python
import pydrc

df = (
    pydrc.data.test_data1()
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
Params3(top=40.50445968423368, bottom=0.3224712712407177, ec50=1.1004776487262973e-07)
```

------------


Multi compound 3-param model.


```python
import pydrc

df = pydrc.data.test_data1().dropna()

drc = pydrc.DRC3()
drc.fit(x=df.conc, y=df.response, c=df.drug)
drc.plot()
```

![pydrc_plot2](https://user-images.githubusercontent.com/10051679/167714692-8f3ff156-234f-4907-9866-d8ba043e270c.png)


```python
print(drc.param_store)
```

```
{
    'A': Params3(top=40.50445968423368, bottom=0.3224712712407177, ec50=1.1004776487262973e-07),
    'B': Params3(top=34.884182594346335, bottom=-0.14824892808869294, ec50=6.994367044164843e-07)
}
```

-----------

Multi compounds 4-parameter model specifying parameter bounds.

```python
import pydrc

df = pydrc.test_data1().dropna()

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
    'A': Params4(top=41.9..., bottom=2.3..., ec50=2.9...e-06, hillslope=0.8...),
    'B': Params4(top=34.7..., bottom=8.9...e-16, ec50=4.7...e-07, hillslope=1.0...)
}
```

