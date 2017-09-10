import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data = np.load('D:/SupiriBot/training_data/training_data.npy')
#train_data = np.load('D:/SupiriBot/training_data.npy')

df = pd.DataFrame(train_data)
#print(df.head())
print(len(train_data))
print(Counter(df[1].apply(str)))


left = []
right = []
fwd = []
bwd = []
stop =[]
end = []

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice[0] == 1:
        fwd.append([img,choice])
    elif choice[1] == 1:
        left.append([img,choice])
    elif choice[2] == 1:
        right.append([img,choice])
    elif choice[3] == 1:
        bwd.append([img,choice])
    elif choice[4] == 1:
        end.append([img,choice])
    elif choice[5] == 1:
        stop.append([img,choice])
    else:
        print('no matches')



print(len(fwd),len(left),len(right),len(bwd),len(end),len(stop))
#
# finaldata = fwd+left+right+bwd+end
#
# shuffle(finaldata)
#
# np.save('D:/SupiriBot/training_data/training_data.npy',finaldata)
