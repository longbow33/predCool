import pandas as pd

minmax = pd.read_csv("minmaxtable.csv")
minmax = minmax.set_index("Att")
print(minmax)
minmax = minmax.swapaxes(1,0)
minmax.to_excel("minmaxtable.xlsx")