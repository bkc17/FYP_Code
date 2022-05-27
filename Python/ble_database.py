# import pyrebase
import firebase_admin
from firebase_admin import db
import multiprocessing as mp
import pygatt
import numpy as np
from threading import Timer
from time import sleep
from signal import signal, SIGINT

class data_upload:
    def __init__(self):
        
        cred_obj = firebase_admin.credentials.Certificate('ServiceAccountKey.json')
        self.default_app = firebase_admin.initialize_app(cred_obj, {
            'databaseURL':"https://fyp-anemometer-default-rtdb.firebaseio.com"
            })
        
        #Initial setting of data
        data = {
        "vdd": [],
        "temp": [],
        "rot_speed": [],
        "grad": []
        }

        self.ref = db.reference("/")
        self.ref.set(data)

        self.rot_speed = []
        self.grad = []

    def call_back(self):
        while self.pipe.poll():
            command = self.pipe.recv()
            if command is None:
                return False
            else:
                self.rot_speed.append(command[2])
                self.grad.append(command[3])
                data = {
                    "vdd": [],
                    "temp": [],
                    "rot_speed": self.rot_speed,
                    "grad": self.grad
                }
        self.ref.update(data)
        return True

    def __call__(self, pipe):
        print("Starting Upload...")
        self.pipe = pipe
        timer = Timer(1, self.call_back)
        timer.start()

class ble:
    def __init__(self):
        self.ble_pipe, upload_pipe = mp.Pipe()
        try:
            self.device = adapter.connect("B0:91:22:0C:61:84")
            print("Connected to turbine!")
        except:
            raise Exception("ERROR: Could not connect to turbine!")

        self.uploader = data_upload()
        self.upload_process = mp.Process(
            target=self.uploader, args=(upload_pipe,), daemon=True)
        self.upload_process.start()
    
    def terminate(self):
        self.adapter.stop()
        print("Goodbye!")
        exit(0)

    def get_data(self, finished = False):
        send = self.ble_pipe.send
        print("hello")
        if finished:
            send(None)
            self.terminate()
        else:
            temp = round((1035 - float(self.device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
            rot_speed = int(self.device.char_read("F000BEEF04514000B000000000000000"))
            grad = int(self.device.char_read("F000BEF004514000B000000000000000"))
            vdd = float(self.device.char_read("F000BEF204514000B000000000000000").decode())/1000
            data = np.array([vdd, temp, rot_speed, grad])
            send(data)

def handler(sig_receieved, frame):
    adapter.stop()
    # save_data_to_excel(save_data_path, y_vdd, y_temp, y_rot_speed, y_grad)
    print('Goodbye!')
    exit(0)


def main():
    ble_obj = ble()
    for _ in range(10000):
        ble_obj.get_data()
        sleep(1)
    ble_obj.get_data(finished = True)


if __name__ == "__main__":
    signal(SIGINT, handler)
    try:
        adapter = pygatt.BGAPIBackend(serial_port = "COM3")
        adapter.start()
        print("Successfully connected to BLED112 adapter at COM3 port")
    except:
        raise Exception ("ERROR: Could not find BLED112 Device! Please verify COM port number in the code.")
    print("hello")
    main()