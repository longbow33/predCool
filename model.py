import torch
import torch.nn as nn

class SISOLSTM(nn.Module):
    def __init__(self, input_size, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hidden_size = 100
        self.num_layers = 5
        self.input_size = input_size
        self.lstm = nn.LSTM(input_size = self.input_size,
                            hidden_size = self.hidden_size,
                            num_layers = self.num_layers,
                            batch_first = True)

        self.layers = nn.Linear(self.hidden_size,1)

    def forward(self,x) -> torch.Tensor:
        x, _ = self.lstm(x)

        x = self.layers(x)
        return x

class MIMOLSTM(nn.Module):
    def __init__(self, input_size, lookback, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hidden_size = 100
        self.num_layers = 5
        self.lookback = lookback
        self.input_size = input_size
        self.lstm = nn.LSTM(input_size = self.input_size,
                            hidden_size = self.hidden_size,
                            num_layers = self.num_layers,
                            batch_first = True)

        self.layers = nn.Sequential(
            nn.Linear(self.hidden_size*self.lookback, self.input_size)
        )

    def forward(self,x) -> torch.Tensor:
        x, _ = self.lstm(x)
        x = torch.reshape(x,(x.shape[0],1,-1))
        x = self.layers(x).squeeze()
        return x