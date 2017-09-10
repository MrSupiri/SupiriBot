import numpy as np
import cv2
import pandas as pd
from collections import Counter
from random import shuffle
import os

train_data = np.load('training_data/training_data.npy',encoding='latin1')

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))


for data in train_data:
	img = data[0]
	speed = data[1]
	cv2.imshow('test',img)
	print (speed)
