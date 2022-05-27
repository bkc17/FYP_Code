import multiprocessing as mp
import random
import time
import pygatt
import random
from multiprocessing import Process, Queue
import firebase_admin
from firebase_admin import db

def ble_get_data(queue):
    try:
        adapter = pygatt.BGAPIBackend(serial_port = "COM3")
        adapter.start()
    except:
        raise Exception("ERROR: Could not find BLED112 adapter! Please check the COM port number.")
    try:
        device = adapter.connect('B0:91:22:0C:61:84')
    except:
        raise Exception("ERROR: Could not connect to the turbine!")

    while True:
        vdd = float(device.char_read("F000BEF204514000B000000000000000").decode())/1000
        temp = round((1035 - float(device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
        rot_speed = int(device.char_read("F000BEEF04514000B000000000000000"))
        grad = int(device.char_read("F000BEF004514000B000000000000000"))
        data = {
            "vdd": vdd,
            "temp": temp,
            "rot_speed": rot_speed,
            "grad": grad
        }
        queue.put(data)
        time.sleep(0.1)

def db_upload(queue):
    cred_obj = firebase_admin.credentials.Certificate('ServiceAccountKey.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':"https://fyp-anemometer-default-rtdb.firebaseio.com"
        })
        
    #Initial setting of data
    data_full = {
    "vdd": [0],
    "temp": [0],
    "rot_speed": [0],
    "grad": [0]
    }

    ref = db.reference("/")
    ref.set(data_full)

    while True:
        if not queue.empty():
            data = queue.get()
            ref.update(data)
            time.sleep(0.5)

def main():
    queue = Queue()  
    ble_process = Process(target=ble_get_data, args=(queue,))
    db_process = Process(target=db_upload, args=(queue,))
    ble_process.start()
    db_process.start()
    ble_process.join()
    db_process.join()

if __name__ == '__main__':
    main()