import os
import time
from argparse import ArgumentParser
import pandas as pd
import matplotlib.pyplot as plt
import torch

from utilities import get_git_root

parser = ArgumentParser()
parser.add_argument("--plot",const=False,nargs="?")
args = parser.parse_args()
plotting = args.plot

git_root = get_git_root()
log_folder = os.path.join(git_root,"XX_logs","logs")


shapes = []
present = [[],[]]
for file in os.listdir(log_folder):
    pt_path = os.path.join(log_folder,file,"logfile.pt")
    xslx_path = os.path.join(log_folder,file,"logfile.xlsx")
    if os.path.exists(pt_path):
        present[0].append(file)
        logfile = torch.load(pt_path)
        print(file, "torch loaded",logfile.shape)
        shapes.append(logfile.shape)
    elif os.path.exists(xslx_path):
        present[0].append(file)
        logfile = pd.read_excel(xslx_path)
        torch.save(logfile,pt_path)
        print(file, "pd loaded and saved to pt",logfile.shape)
        shapes.append(logfile.shape)
    else:
        present[1].append(file)
        time.sleep(1)
        continue
    
    if logfile.shape[0] < 10000:
        print(file, "IS TOO SMALL\n\n")

    if plotting:
        # plot the flightpath
        plt.title(file)
        x = logfile["Lat"]
        y = logfile["Lng"]
        plt.plot(x,y,"red")
        plt.show()

sum_timepoints = sum([x[0] for x in shapes])

print("Sum of all timepoints: ", sum_timepoints)
