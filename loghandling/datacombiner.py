import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
from bisect import bisect_left
from tqdm import tqdm
from argparse import ArgumentParser
import git
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--log")

args = parser.parse_args()


log_types = ["AETR","AHR2","GPS","IMU"]
log = args.log
cwd  = os.getcwd()
git_root = git.Repo(cwd,search_parent_directories= True)
git_root = Path(git_root.git.rev_parse("--show-toplevel"))
log_folder = os.path.join(git_root,"XX_logs","logs")

if os.path.exists(os.path.join(log_folder,log,"logfile.xlsx")):
    print("already done", log)
    exit()

log_list = []
for typ in log_types:
    typ = str(typ)+".csv"
    log_path = os.path.join(log_folder,log,typ)
    log_list.append(pd.read_csv(log_path))

num_timestamps = [len(list(log_list[x].timestamp)) for x in range(len(log_types))]


verbose = True
if verbose:
    for iter,typ in enumerate(log_list):
        x = typ.timestamp
        y = [iter for _ in typ.timestamp]
        #plt.scatter(x,y,marker='.')
        #plt.show()

    for iter,typ in enumerate(log_list):
        print(log_types[iter], end=" -> ")
        print(len(list(typ.timestamp))," entries\nfirst 5 timestamp entries:")
        for i in range(5):
            print(datetime.fromtimestamp(typ.timestamp[i]))

        print("----------------")

## construct all params
all_params = []
for type in log_list:
    [all_params.append(x) for x in type.columns if x not in all_params]


def take_closest(myList,myNumber):
    pos = bisect_left(myList,myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    return myList[pos]

## construct dataframe
full_data = pd.DataFrame(columns=all_params).drop("TimeUS",axis=1).set_index("timestamp")

print(full_data)
tempdf = full_data

timestamps = []

for time_point in tqdm(log_list[0].timestamp):

    ## for every timestamp
    tempdict = full_data.to_dict()

    data = log_list[0][log_list[0]["timestamp"] == time_point].head().set_index("timestamp").to_dict()
    
    for key in data:
        tempdict[key] = data[key]

    for iter,type in enumerate(log_list[1:]):
        closest = take_closest(list(type.timestamp),time_point)
        data = type[type["timestamp"] == closest].head()
        data["timestamp"] = time_point
        data = data.drop(["TimeUS"],axis = 1).set_index("timestamp").to_dict()
        for key in data:
            tempdict[key] = data[key]
        
    newdf = pd.DataFrame.from_dict(tempdict)

    
    tempdf = pd.concat([tempdf,newdf])
    
savefilepath = os.path.join(log_folder,log,"logfile.xlsx")
tempdf.to_excel(savefilepath)
print("done")
