import os
from random import shuffle

import numpy as np

from models import *

# what to start at
starting_file_number = 0

# what to end at
ending_file_number = 2

# use a previous model to begin?
START_FRESH = True

WIDTH = 80
HEIGHT = 60
LR = 1e-4
cnn_name = 'alexnet'
hm_data = '53K'
output = 6

MODEL_NAME = 'SupiriBot-{}({}x{})-{}-{}-{}'.format(cnn_name,WIDTH,HEIGHT,LR,hm_data,output)

model = alexnet(WIDTH, HEIGHT, LR, output)

if not START_FRESH and os.path.isfile('{}.meta'.format(MODEL_NAME)):
    model.load(MODEL_NAME)
    print('Model Loaded')



for i in range(starting_file_number,ending_file_number+1):
    try:
        train_data = np.load('D:/SupiriBot/training_data/Stage 1/training_data-{}.npy'.format(i))
        # shuffle(train_data)
        # test_size = int(len(train_data) / 10)
        # train = train_data[:-test_size]
        # test = train_data[-test_size:]


        X = np.array([i[0] for i in train_data]).reshape(-1, WIDTH, HEIGHT, 1)
        Y = [i[1] for i in train_data]
        #
        # test_x = np.array([i[0] for i in test]).reshape(-1, 80, 80, 1)
        # test_y = [i[1] for i in test]


        # model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
        #           snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)

        model.fit(X, Y, n_epoch=10, validation_set=0.1, shuffle=True,
                  show_metric=True, snapshot_step=200,
                  snapshot_epoch=False, run_id=MODEL_NAME)

        model.save(MODEL_NAME)

    except Exception as e:
        print(str(e))

    # tensorboard --logdir=supiribot:D:\SupiriBot\train_model
