# pyDRC

Dose response curve fitting in python.


## examples


Single compound 3-param model.


input:
```python
import pydrc


df = pydrc.data.test_data1().dropna()
df_a = df[df.drug == "A"]

drc = pydrc.DRC3()
drc.fit(x=df_a.conc, y=df_a.response)

print(df.head())

print(drc.param_store)
```

output:
```
        conc  response drug
1.000000e-10       0.0    A
1.000000e-08       1.0    A
3.000000e-08      12.0    A
1.000000e-07      19.0    A
3.000000e-07      28.0    A
```

```
Params3(top=40.50445968423368, bottom=0.3224712712407177, ec50=1.1004776487262973e-07)
```

------------


Multi compound 3-param model.


input:
```python
import pydrc


df = pydrc.data.test_data1().dropna()

drc = pydrc.DRC3()
drc.fit(x=df.conc, y=df.response, c=df.drug)
drc.plot()

print(drc.param_store)
```

output:
![pydrc_plot2](https://user-images.githubusercontent.com/10051679/167714692-8f3ff156-234f-4907-9866-d8ba043e270c.png)

```
{
    'A': Params3(top=40.50445968423368, bottom=0.3224712712407177, ec50=1.1004776487262973e-07),
    'B': Params3(top=34.884182594346335, bottom=-0.14824892808869294, ec50=6.994367044164843e-07)
}
```

