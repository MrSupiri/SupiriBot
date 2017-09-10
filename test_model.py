import _pickle as pickle
import socket
import time
import cv2
from SupiriBot import *
from models import *

model = alexnet(WIDTH, HEIGHT, LR, output=6)

if os.path.isfile('D:/SupiriBot/train_model/{}.meta'.format(MODEL_NAME)):
    model.load('D:/SupiriBot/train_model/' + MODEL_NAME)
    print('Model Loaded')

def start_server():
    HOST = '192.168.1.100'
    PORT = 5000
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    try:
        conn.bind((HOST, PORT))
    except socket.error:
        print('Bind failed')
        return False

    conn.listen(5)
    print('Socket awaiting messages')
    (conn, addr) = conn.accept()
    print('Connected')
    return conn

def mainloop( last_time = time.time() ):
    conn = start_server()
    while 1:
        try:
            data = conn.recv(5200)
            img = np.array(pickle.loads(data))
            model_out = model.predict([img.reshape(WIDTH, HEIGHT, 1)])[0]
            prediction = np.argmax(model_out)
            cv2.imshow('image', cv2.resize(img, (240, 180)))
            conn.send(pickle.dumps(prediction))
            model_out=list(model_out)
            print('Loop Took', round(time.time() - last_time, 3), "sec , Model's Prediction :", model_out)
            last_time = time.time()
        except Exception as e:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

while 1:
    try:
        mainloop()
    except:
        cv2.destroyAllWindows()
        print('Something Went Wrong Restarting')