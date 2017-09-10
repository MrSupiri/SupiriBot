import numpy as np
from random import shuffle

training_data =[]

for i in range(0,14):
    training_data += list(np.load('D:/SupiriBot/training_data/row_data/Stage 1/training_data-{}.npy'.format(i)))

# size = len(training_data)
#
# i=0
# while size > 5000:
#     np.save('D:/SupiriBot/training_data/Stage 1/training_data-{}.npy'.format(i),training_data[i:5000])
#     size -= 5000
#     i+=5000
#
# np.save('D:/SupiriBot/training_data/Stage 1/training_data-{}.npy'.format(i),training_data[i:])
#
batch_size = 5000
shuffle(training_data)
i=0
inc = 0
print(len(training_data))
while i < len(training_data):
    start = i
    end = i + batch_size
    np.save('D:/SupiriBot/training_data/Stage 1/training_data-{}.npy'.format(inc), training_data[start:end])
    i += batch_size
    inc+=1