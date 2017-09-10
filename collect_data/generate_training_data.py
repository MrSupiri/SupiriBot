import cv2
import random
from SupiriBot import *

hm_batches = 15

img = np.zeros((60, 80), np.int8)
img = np.array(img, dtype=np.uint8)

change = 15
linewidth = -1
count = 1
inc = 1

z = 20

def strightline():
    change = 3
    x = random.randint(30 - change, 30 + change)
    cv2.rectangle(img, (x, 0), (x+z, 80), (255, 255, 255), linewidth)

def left():
    x = random.randint(-10, 25)
    cv2.rectangle(img, (x, 0), (x+z, 80), (255, 255, 255), linewidth)

def right():
    x = random.randint(50, 80)
    cv2.rectangle(img, (x, 0), (x+z, 80), (255, 255, 255), linewidth)

def deadend():
    x = random.randint(30 - change, 30 + change)
    y = random.randint(30 - change, 30 + change)
    cv2.rectangle(img, (x, y), (x+z, 80), (255, 255, 255), linewidth)

def r90():
    x = random.randint(-10, 70)
    y = random.randint(-5, 50)
    cv2.rectangle(img, (x, y), (x+z, 80), (255, 255, 255), linewidth)
    cv2.rectangle(img, (x, y), (80, y+z), (255, 255, 255), linewidth)

def l90():
    x = random.randint(-10, 70)
    y = random.randint(-10, 50)
    cv2.rectangle(img, (x, y), (0, y+z), (255, 255, 255), linewidth)
    cv2.rectangle(img, (x, y), (x+z, 80), (255, 255, 255), linewidth)

def t_jun():
    x = random.randint(-10, 70)
    y = random.randint(-10, 50)
    cv2.rectangle(img, (x, y), (x+z, 80), (255, 255, 255), linewidth)
    cv2.rectangle(img, (-10, y), (80, y+z), (255, 255, 255), linewidth)

def t_jun_R():
    x = random.randint(-10, 70)
    y = random.randint(-10, 50)
    cv2.rectangle(img, (x, 0), (x+z, 80), (255, 255, 255), linewidth)
    cv2.rectangle(img, (x, y), (80, y+z), (255, 255, 255), linewidth)

def t_jun_L():
    x = random.randint(-10, 70)
    y = random.randint(-10, 50)
    cv2.rectangle(img, (x, 0), (x+z, 80), (255, 255, 255), linewidth)
    cv2.rectangle(img, (0, y), (x+z, y+z), (255, 255, 255), linewidth)

def stop():
    x = random.randint(35 - change, 35 + change)
    y = random.randint(45, 60)
    cv2.rectangle(img, (-50, -50), (80, y), (255, 255, 255), linewidth)
    cv2.rectangle(img, (x, 0), (x + z, 80), (255, 255, 255), linewidth)
    cv2.rectangle(img, (x, y-20), (x+20, y), (0, 0, 0), linewidth)

def addnoice(addmore=False):
    if addmore:
        k = 75
    else:
        k = 250

    for _ in range(0,random.randint(0,k)):
        x = random.randint(0,80)
        y = random.randint(0,80)
        cv2.circle(img, (x, y), 1, (255, 255, 255), -1)
    for _ in range(0,random.randint(0,k)):
        x = random.randint(0,80)
        y = random.randint(0,80)
        cv2.circle(img, (x, y), 1, (0, 0, 0), -1)

def makeaframe(img):
    if inc == 0:
        output = FWD
        strightline()
    elif inc == 1:
        output = LEFT
        left()
    elif inc == 2:
        output = RIGHT
        right()
    elif inc == 3:
        output = TURN
        deadend()
    elif inc == 4:
        output = RIGHT
        r90()
    elif inc == 5:
        output = LEFT
        l90()
    elif inc == 6:
        output = RIGHT
        t_jun()
    elif inc == 7:
        output = FWD
        t_jun_L()
    elif inc == 8:
        output = RIGHT
        t_jun_R()
    else:
        output = END
        stop()

    if count % 100 == 0:
        addnoice(True)
    else:
        addnoice(False)

    balbal = random.randint(0, 7)

    if balbal < 3:
        angle = 0
    elif balbal > 3 and balbal < 6:
        angle = random.randint(-15, 15)
    else:
        angle = random.randint(-35, 35)

    M = cv2.getRotationMatrix2D((40, 30), angle, 1)
    img = cv2.warpAffine(img, M, (80, 60))

    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)

    return img,output

training_data,starting_value = train_data()
file_name = 'training_data/training_data-{}.npy'.format(starting_value)

while True:
    cv2.rectangle(img, (0, 0), (80, 60), (0, 0, 0), -1)

    processedimage, output = makeaframe(img)
    training_data.append([np.array(processedimage), output])

    if len(training_data) % int(batch_size/10) == 0:
        print(len(training_data))
        if len(training_data) == batch_size:
            np.save(file_name, training_data)
            print('\nSAVED')
            training_data = []
            starting_value += 1
            file_name = 'training_data/training_data-{}.npy'.format(starting_value)

    if starting_value == hm_batches:
        break

    count += 1
    inc += 1
    if inc > 9:
        inc = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
