import matplotlib.pyplot as plt
from loader import Loader
from compressor import Compressor
try:
    import torch
except ImportError:
    print("pytorch not available")

NUM_POINTS = 8
DATA_PERCENTAGE = .02 ## for testing no need to take the full data

loader = Loader(32)


full_data = loader.load()
# cut data to half the length
print("full line count: ",len(full_data.values), "quotient: ", int(1/DATA_PERCENTAGE))
linecount = int(len(full_data.values)//(1/DATA_PERCENTAGE))
print("line count", linecount)
full_data = full_data.head(linecount)

c = Compressor(full_data,NUM_POINTS)

compressed_data = c.generate_compressed_data()



for step, datapoint in enumerate(compressed_data):
    thr_ground_truth = datapoint[-1]
    thr_ground_truth.reverse()

    plt.plot(range(NUM_POINTS),thr_ground_truth,"red")
    #plt.plot(range(NUM_POINTS),datapoint[6],"blue")
    #plt.plot(range(NUM_POINTS),datapoint[7],"green")
    plt.plot([x+NUM_POINTS-1 for x in range(NUM_POINTS)],datapoint[2],"blue")
    plt.axis([0,NUM_POINTS*2,0,120])
    plt.grid(True)
    plt.title("future thr: red, past throttle: blue")
    plt.pause(0.001)
    plt.clf()
print("done")
plt.show()
