"""
Module To compress the data in a shorter array,
giving datapoints in the present more weight
"""
from statistics import mean, StatisticsError
from utilities import sliceable_deque
from tqdm import tqdm
from loader import Loader
import torch

class Compressor():

    def __init__(self, data,num_points=4) -> None:
        self.data = data
        self.index = 0
        self.num_points = num_points
        self.queues = []
        for _ in self.data:
            self.queues.append(sliceable_deque([0 for _ in range(2*(2**num_points))],maxlen= 2*(2**num_points)))

        self.gen = iter(self.data.values)
        self.compressed_data = []

    def generate_compressed_data(self):
        """
        compresses the full length of the data
        parameters:
            None
        returns:
            compressed data (3 dimensional list): the compressed data
        """
        for it, line in enumerate(tqdm(self.data.values,desc= "Compressing Data: ")):
            ## iterating over whole data
            ## filling queue with newest datapoints
            _ = [self.queues[i].appendleft(obj) for i,obj in enumerate(line)]
            future_data = []
            past_data = []
            for i in self.queues:
                temp_list_future = []
                temp_list_past = []
                for j in range(self.num_points):
                    past_upper = (2**self.num_points)+(2**(j+1))
                    past_lower = (2**self.num_points)+(2**j)
                    future_upper = (2**self.num_points)-(2**j)
                    future_lower = (2**self.num_points)-(2**(j+1))
                    temp_list_future.append(mean(list(i[future_lower:future_upper])))
                    temp_list_past.append(mean(list(i[past_lower:past_upper])))
                future_data.append(temp_list_future)
                past_data.append(temp_list_past)
            past_with_thr_preds = past_data
            past_with_thr_preds.append(future_data[2])
            self.compressed_data.append(past_with_thr_preds)
        print("compressed")
        self.compressed_data = torch.Tensor(self.compressed_data)
        return self.compressed_data


if __name__ == "__main__":
    ## for testing
    loader = Loader(32)
    data = loader.load()
    c = Compressor(data)
    c.generate_full_data()