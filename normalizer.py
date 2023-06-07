import os
import torch
from torch import nn
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn import preprocessing
import random

from utilities import get_git_root

class normalizer():
    def __init__(self, att) -> None:
        self.attributes = att
        
@staticmethod
def normalize(data) -> pd.DataFrame: 
    minmaxtable = pd.read_excel(
        os.path.join(get_git_root(),"minmaxtable.xlsx"),
        index_col=0
    )
    for att in data:
        att_min, att_max = minmaxtable[att]
        data[att] = (data[att]-att_min)/(att_max-att_min)
    return data
