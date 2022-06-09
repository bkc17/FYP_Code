import multiprocessing as mp
import time
import pygatt
from multiprocessing import Process, Queue
import firebase_admin
from firebase_admin import db, storage
import csv
import os
import pandas as pd
from math import sqrt


def calc_wind_speed(a, b, c):
    d = (b**2) - (4*a*c)
    if(d >= 0):
        sol2 = (-b-sqrt(d))/(2*a)  
        sol1 = (-b+sqrt(d))/(2*a)
        if(sol1>=0):
            return round(sol1,2)
        return round(sol2,2)
    return 0

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
            

            a = 0.625
            b = -0.0531 - 0.00363*rot_speed
            c = -2.591 -0.0239*rot_speed +0.408*grad
            wind_speed = calc_wind_speed(a, b, c)

            data = {
                "vdd": vdd,
                "temp": temp,
                "rot_speed": rot_speed,
                "grad": grad,
                "wind_speed": wind_speed
            }

            queue.put(data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        adapter.stop()
        # save_data()
        print("Goodbye!")
        
def save_data(vdd, temp, rot, grad, wind_speed):
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
    df["Wind Speed"] = wind_speed

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
        # "Full data":
        #     {
        #     "VDD": [0],
        #     "Temperature": [0],
        #     "Rotation Speed": [0],
        #     "Gradient": [0]
        #     },
        "data_current":
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
        wind_full = []

        while True:
            if not queue.empty():
                data = {}
                rec = queue.get()
                vdd_full.append(rec["vdd"])
                temp_full.append(rec["temp"])
                rot_full.append(rec["rot_speed"])
                grad_full.append(rec["grad"])
                wind_full.append(rec["wind_speed"])

                data["Current data"] = rec
                # data["Full data"] = {
                #     "VDD": vdd_range,
                #     "Temperature": temp_range,
                #     "Rotation Speed": rot_range,
                #     "Gradient": grad_range
                # }
                ref.update(data)
                time.sleep(0.5)
    except KeyboardInterrupt:
        save_data(vdd_full, temp_full, rot_full, grad_full, wind_full)

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
