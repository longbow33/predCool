# predCool

## NOTES:

### try to predict the throttle just by passed throttle

### try to predict the throttle just one step at a time

- done, diverging very fast, next step is to use more data

### try to predict the throttle by using non- compressed

- better idea in general, adjust the lookback and watch the performance

## TODO

### General good Tip:

- try to overfit your data on a smaller batchsize to see if model is capable of learning data

- [ ] plot a graph of the last 20 losses or similar to view trend even if outlier is at the start of training

### SISOLSTM

- [x] use more data to train the SISOLSTM model
  
  - increased batchsize from 102 to 1000, learning time ~ 40 min
  - used full data from all useful flights, 1 mio datapoints
  
  -> still no improvements

- [x] use more LOOKBACK to train

- [ ] much better, train with even more lookback ?

### MISOLSTM

- [ ] MISOLSTM would be possible if the number of predictes values is equal to the lookback values

- [ ] rigid version, since you cant parametrize the number of predicted values
  
  - could be sufficient since you can predict more values and then take less values
  
  - maybe cheaper in training time than MIMOLSTM

### MIMOLSTM

- [ ] miso is not feasible since the recursive prediction needs all attributes

- [x] train MISOLSTM model with fewer attributes of the logs (Control Inputs, GyRs etc.) -> make sure that the input format is correct, LSTM might expect the time series direction to be in a certain direction.

- [x] huge training times
  
  - [ ] reduce attributes?
  
  - [ ] reduce layers of lstm ?

- [ ] first try -> second try: learning rate *10

- [x] try to rearrange model to just predict one timestep at a time
  
  - good training performance
  
  - [ ] test

### GENERAL

- [ ] refactor code, remove duplicated files and improve structure
  
  - [ ] maybe put the loghandling into the utilities file, avoid using os.system to run them
  - [x] delete all duplicates
  - [x] move loghandling into log handling folder ?
  - [ ] utilities file is duplicate because of imports from parent folder not possible (look it up)

- [x] remove BARO from the data, if existing (not every logfile has it and it carries minimal information if any) 
  
  - carries the ground temperature, not very useful since start temp is not that important
  
  - [ ] write script to automate it, use listdir to ease iterating over the folders
    
    - load and save, maybe add the battery data to the file while you are at it

- [ ] loader class might be unnecessary due to the capabilities of the torch module being able to load and save tensors and dataframes faster and easier
  
  - [ ] change loader class to make sure it uses the torch module to load

- [ ] include BAT logs to monitor the current (?)
  
  - [ ] first see the data to ensure it is useful
