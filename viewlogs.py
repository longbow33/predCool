import pandas as pd
import json
import matplotlib.pyplot as plt

df = pd.read_json("out.json", lines = True, chunksize=1000)

for chunk in df:
    dat = chunk["data"][0]
    for key in dat.keys():
        print(key, dat[key])