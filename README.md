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

- [x] plot a graph of the last 20 losses or similar to view trend even if outlier is at the start of training

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
  
  - acceptable performance in steady level unaccelerated flight, edge cases bad performance

- [ ] make edge cases more prominent by making every % of throttle equally probable

### END TO END

- Rules:
  
  - INPUT:
    
    - Passed Flightdata
    
    - Passed Heat
    
    - Current Fluid Flow
  
  - OUTPUT:
    
    - Increase / Decrease Fluid Flow
    
    - or increase / reduce heat taken from system (might be better to get around heat calculations)
  
  - LOSS:
    
    - Desired Heat, Current Heat ?
    
    - has to take into account the future expected heat ?

- LSTM ? no time series prediction really

- trainloop just run the data through and thats it ?

### GENERAL

- [x] refactor code, remove duplicated files and improve structure
  
  - [ ] maybe put the loghandling into the utilities file, avoid using os.system to run them
  - [x] delete all duplicates
  - [x] move loghandling into log handling folder ?
  - [x] utilities file is duplicate because of imports from parent folder not possible (look it up)

- [x] remove BARO from the data, if existing (not every logfile has it and it carries minimal information if any) 
  
  - carries the ground temperature, not very useful since start temp is not that important
  
  - [ ] write script to automate it, use listdir to ease iterating over the folders
    
    - load and save, maybe add the battery data to the file while you are at it

- [ ] loader class might be unnecessary due to the capabilities of the torch module being able to load and save tensors and dataframes faster and easier
  
  - [ ] change loader class to make sure it uses the torch module to load

- [ ] include BAT logs to monitor the current (?)
  
  - [ ] first see the data to ensure it is useful

- Similar to end to end approach: is just the next data point of interest ?
  
  - control just acts from one point to another
  
  - reduce computing time
  
  - no, if fluid flow is sluggish you have to plan ahead more
  
  - yes, predictions are too fickle to trust them, maybe adjust training to make points in the nearer future more reliable ?

### Data Normalisation

- [ ] View minimum and maximum values of data
  
  | Att   | Min     | Max    | ChosenMin | ChosenMax |
  | ----- | ------- | ------ | --------- | --------- |
  | Thr   | 0       | 100    | 0         | 100       |
  | Ail   | -4500   | 4500   | -4500     | 4500      |
  | Elev  | -4500   | 4500   | -4500     | 4500      |
  | Rudd  | -4500   | 4500   | -4500     | 4500      |
  | Roll  | -179.92 | 179.92 | -180      | 180       |
  | Pitch | -89.8   | 77.85  | -90       | 90        |
  | Yaw   | 0       | 0      | 0         | 1         |
  | Spd   | 0       | 46.4   | 0         | 60        |
  | GyrX  | -3.96   | 4.77   | -15       | 15        |
  | GyrY  | -3.55   | 12.06  | -15       | 15        |
  | GyrZ  | -10.77  | 4.44   | -15       | 15        |
  | AccX  | -129.83 | 43     | -150      | 150       |
  | AccY  | -69.72  | 82.33  | -150      | 150       |
  | AccZ  | -111.96 | 12.60  | -150      | 150       |
