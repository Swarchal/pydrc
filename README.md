# pyDRC

Dose response curve fitting in python.


## examples

```python
import pydrc


df = pydrc.data.test_data1().dropna()
df_a = df[df.drug == "A"]

drc = pydrc.DRC3()
drc.fit(x=df_a.conc, y=df_a.response)
drc.model_store
```

```
Params3(top=40.50445968423368, bottom=0.3224712712407177, ec50=1.1004776487262973e-07)
```



```python
import pydrc


df = pydrc.data.test_data1().dropna()

drc = pydrc.DRC3()
drc.fit_plot(x=df.conc, y=df.response, c=df.drug)
```

![pydrc_plot2](https://user-images.githubusercontent.com/10051679/167714692-8f3ff156-234f-4907-9866-d8ba043e270c.png)
