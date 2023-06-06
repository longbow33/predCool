import random
import torch

class Diversifyer:
    """
    class to diversify the data
    """
    def __init__(self, num_sets :int) -> None:
        self.num_sets = num_sets
        self.max_thr = 100

    def diversify(self,dataset) -> torch.Tensor:
        """
        diversifies the data, so that each percentage will be represented
        equally
        inputs:
            dataset (torch.tensor): the input dataset
        returns:
            dataset (torch.tensor): the diversified dataset
        """

        # WORK WITH TENSORS DUMBASS
        # desired shape:
        # inner data: 48x10 (48 attributes x 10 timeseries)
        # for each percent of throttle -> 101 x 48 x 10
        # ten sets -> 10 x 101 x 48 x 10

        returnset = torch.zeros([self.num_sets,self.max_thr+1,48,10])
        print(returnset.shape)

        split_up_data = [[] for _ in range(self.max_thr+1)]

        for entry in dataset:
            
            thr = int(entry[-1][0])
            split_up_data[thr].append(entry)

        for it1 in range(self.num_sets):
            for it2 in range(self.max_thr+1):
                returnset[it1,it2,:,:] = random.choice(split_up_data[it2])

        return returnset
