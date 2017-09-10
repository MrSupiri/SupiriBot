import time
import socket
import _pickle as pickle
from SupiriBot import *


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
    print('Socket awaiting handshake')
    (conn, addr) = conn.accept()
    print('Connected')
    return conn


def keys_to_output(keys):
    output = STAY
    if 'W' in keys:
        output = FWD
    elif 'A' in keys:
        output = LEFT
    elif 'D' in keys:
        output = RIGHT
    elif 'S' in keys:
        output = BACK
    elif 'T' in keys:
        output = TURN
    elif 'G' in keys:
        output = END
    return output

def mainloop():
    training_data, starting_value = train_data()
    file_name = '../training_data/training_data-{}.npy'.format(starting_value)
    conn = start_server()
    paused = True
    last_time = time.time()
    while 1:
        data = conn.recv(5200)
        try:
            img = np.array(pickle.loads(data))
            keys = key_check()
            cv2.imshow('image', cv2.resize(img, (240, 180)))
            output = keys_to_output(keys)

            if not paused and output != STAY:
                training_data.append([img, output])
                if len(training_data) % 100 == 0:
                    print(len(training_data))
                    np.save(file_name, training_data)
                    if len(training_data) == batch_size:
                        starting_value+=1
                        print('Separating Batch, Start Writing to training_data-{}.npy'.format(starting_value))
                        training_data = []
                        file_name = '../training_data/training_data-{}.npy'.format(starting_value)
            # drawLines(img)
            # cv2.imshow('image2', cv2.resize(img, (240, 180)))


            data = pickle.dumps(output)
            conn.send(data)

            print('Loop Time:', round((time.time() - last_time),4), output, len(training_data), 'Paused State:',paused)
            last_time = time.time()

            if 'P' in keys:
                if paused:
                    paused = False
                    print('Unpaused!')
                    time.sleep(1)
                else:
                    print('Pausing!')
                    paused = True
                    time.sleep(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)
    cv2.destroyAllWindows()

while 1:
    try:
        mainloop()
    except Exception as e:
        cv2.destroyAllWindows()
        print('Something Went Wrong Restarting')
        print(e)