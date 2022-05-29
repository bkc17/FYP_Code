import multiprocessing as mp
import time
import pygatt
from multiprocessing import Process, Queue
import firebase_admin
from firebase_admin import db, storage
import csv
import os
import pandas as pd

def ble_get_data(queue):
    try:
        try:
            adapter = pygatt.BGAPIBackend(serial_port = "COM3")
            adapter.start()
            print("Found BLED112 adapter!")
        except:
            raise Exception("ERROR: Could not find BLED112 adapter! Please check the COM port number.")
        try:
            device = adapter.connect('B0:91:22:0C:61:84')
            print("Connected to turbine successfully!")
        except:
            raise Exception("ERROR: Could not connect to the turbine!")

        print("Reading data...")
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
    except KeyboardInterrupt:
        adapter.stop()
        # save_data()
        print("Goodbye!")
        
def save_data(vdd, temp, rot, grad):
    print("Saving data...")
    file = "final_results.csv"

    #Deleting old data file if it exists
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("Deleting old data_files")

    #Creating a dataframe for easy conversion to csv
    fields = ["VDD", "Temperature", "Rotation Speed", "Gradient"]
    df = pd.DataFrame(columns = fields)
    df["VDD"] = vdd
    df["Temperature"] = temp
    df["Rotation Speed"] = rot
    df["Gradient"] = grad

    #Converting the dataframe to CSV
    df.to_csv("final_results.csv")

    #Storing the CSV File on firebase storage
    store = storage.bucket()

    store = store.blob("final_results.csv")
    store.upload_from_filename("final_results.csv")

def db_upload(queue):
    try:
        cred_obj = firebase_admin.credentials.Certificate('ServiceAccountKey.json')
        default_app = firebase_admin.initialize_app(cred_obj, {
            "databaseURL":"https://fyp-anemometer-default-rtdb.firebaseio.com",
            "storageBucket": "fyp-anemometer.appspot.com"
            })
            
        #Initial setting of data
        data_full = {
        "Full data":
            {
            "VDD": [0],
            "Temperature": [0],
            "Rotation Speed": [0],
            "Gradient": [0]
            },
        "Current data":
            {
                "VDD": 0,
                "Temperature": 0,
                "Rotation Speed": 0,
                "Gradient": 0
            }
        }

        ref = db.reference("/")
        ref.set(data_full)
        vdd_full = []
        temp_full = []
        rot_full = []
        grad_full = []

        while True:
            if not queue.empty():
                data = {}
                rec = queue.get()
                vdd_full.append(rec["vdd"])
                temp_full.append(rec["temp"])
                rot_full.append(rec["rot_speed"])
                grad_full.append(rec["grad"])

                vdd_range = vdd_full[-10:]
                temp_range = temp_full[-10:]
                rot_range = rot_full[-10:]
                grad_range = grad_full[-10:]

                data["Current data"] = rec
                data["Full data"] = {
                    "VDD": vdd_range,
                    "Temperature": temp_range,
                    "Rotation Speed": rot_range,
                    "Gradient": grad_range
                }
                ref.update(data)
                time.sleep(0.5)
    except KeyboardInterrupt:
        save_data(vdd_full, temp_full, rot_full, grad_full)

def main():
    try:
        queue = Queue()  
        ble_process = Process(target=ble_get_data, args=(queue,))
        db_process = Process(target=db_upload, args=(queue,))
        ble_process.start()
        db_process.start()
        ble_process.join()
        db_process.join()
    except KeyboardInterrupt:
        db_process.terminate()
        ble_process.close()
        exit(0)

if __name__ == '__main__':
    main()
