import os
import numpy as np
import cv2


batch_size = 4000
WIDTH = 80
HEIGHT = 60
LR = 1e-4
cnn_name = 'alexnet'
hm_data = '53K'
output = 6


FWD     = [1, 0, 0, 0, 0, 0]
LEFT    = [0, 1, 0, 0, 0, 0]
RIGHT   = [0, 0, 1, 0, 0, 0]
BACK    = [0, 0, 0, 1, 0, 0]
TURN    = [0, 0, 0, 0, 1, 0]
END     = [0, 0, 0, 0, 0, 1]
STAY    = [0, 0, 0, 0, 0, 0]

MODEL_NAME = 'SupiriBot-{}({}x{})-{}-{}-{}'.format(cnn_name,WIDTH,HEIGHT,LR,hm_data,output)


def train_data(fileNumber=0, restart=False):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    while True:
        if restart:
            dirPath = "training_data"
            fileList = os.listdir(dirPath)
            for fileName in fileList:
                os.remove(dirPath + "/" + fileName)
        file_name = 'training_data/training_data-{}.npy'.format(fileNumber)
        if os.path.isfile(file_name) and len(np.load(file_name)) == batch_size:
            print('training_data-{}.npy exists, checking next file'.format(fileNumber))
            fileNumber += 1
        else:
            print('Start Writing to training_data-{}.npy'.format(fileNumber))
            if os.path.isfile(file_name):
                training_data = list(np.load(file_name))
            else:
                training_data = []
            break
    return training_data,fileNumber



# Citation: Box Of Hats (https://github.com/Box-Of-Hats )
import win32api as wapi


keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys