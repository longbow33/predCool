import collections
import itertools
import os
import matplotlib.pyplot as plt
from pathlib import Path
import random
import torch
import pandas as pd
import git
from tqdm import tqdm

class sliceable_deque(collections.deque):
    def __getitem__(self, index):
        try:
            return collections.deque.__getitem__(self, index)
        except TypeError:
            return type(self)(itertools.islice(self, index.start,
                                               index.stop, index.step))

@staticmethod
def prepare_data(data: pd.DataFrame, lookback: int) -> torch.Tensor:
    """
    constructs tensor applying a lookback to the data
    inputs:
        data: torch.Tensor 1d
        lookback: int amount of datapoints in the past to send with
    
    returns:
        data: torch.Tensor 2d
        newest point is on the right side!
    """
    lookback +=1
    data = torch.Tensor(data.values).squeeze()

    res_tens = torch.zeros(data.shape[0]-lookback,lookback)

    print("preparing data")
    for i, _ in tqdm(enumerate(data,lookback)):
        try:
            res_tens[i,:] = data[i-lookback:i]
        except IndexError:
            continue

    return res_tens


@staticmethod
def get_git_root():
    """
    returns the root of the git repository it is called in
    """ 
    cwd = os.getcwd()
    git_root = git.Repo(cwd,search_parent_directories= True)
    git_root = Path(git_root.git.rev_parse("--show-toplevel"))
    return git_root

@staticmethod
def normalize(data) -> pd.DataFrame: 
    """
    returns a normalized version of the data according
    to the minima and maxima givein in minmaxtable.xlsx
    """
    minmaxtable = pd.read_excel(
        os.path.join(get_git_root(),"minmaxtable.xlsx"),
        index_col=0
    )
    for att in data:
        att_min, att_max = minmaxtable[att]
        data[att] = (data[att]-att_min)/(att_max-att_min)
    return data

@staticmethod
def pick_places(data: torch.Tensor,lookback = 100,normalisation_fac = 1) -> list:
    places_sorted = [[] for _ in range(101)]

    print("diversifying")
    for it, entry in enumerate(tqdm(data)):
        thr_val = int(entry[0]*normalisation_fac)
        places_sorted[thr_val].append(it)
    
    [print(min(x)) for x in places_sorted if min(x) < lookback]

    return places_sorted
