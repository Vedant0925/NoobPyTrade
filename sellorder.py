import numpy as np
deltas = []
for i in range(1, len(train_test_records)):
    deltas += [abs(train_test_records[i]['close']-train_test_records[i-1]['close'])]
    
delta = np.percentile(deltas, 75)
print(delta)
