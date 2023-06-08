import torch
import pandas as pd
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

from utilities import get_git_root
LOG_FOLDER = os.path.join(get_git_root(),"XX_logs","logs")
LOGS = os.listdir(LOG_FOLDER)

full_logs = []

for log in tqdm(LOGS):
    full_logs.append(torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")))

topick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]

full_logs = pd.concat(full_logs)
full_logs = full_logs[topick]
logs_vals = full_logs.values

logs_sorted = [[]for _ in range(101)]

for it, entry in enumerate(logs_vals):
    thr_val = int(entry[0])
    logs_sorted[thr_val].append(it)

for i, entry in enumerate(logs_sorted):
    print(i,": ",len(entry))

plt.plot([len(x) for x in logs_sorted])
plt.grid(True)
plt.title("Throttle Percentage Distribution")
plt.xlabel("Throttle Percentage")
plt.ylabel("Number of entries")
plt.savefig("throttle_percentage_distribution.png")
plt.show()