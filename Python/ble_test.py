import pygatt
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import threading
from signal import signal, SIGINT
from sys import exit


def ble_read_data(device):
    vdd = float(device.char_read("F000BEF204514000B000000000000000").decode())/1000
    temp = round((1035 - float(device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
    rot_speed = int(device.char_read("F000BEEF04514000B000000000000000"))
    grad = int(device.char_read("F000BEF004514000B000000000000000"))

    return vdd, temp, rot_speed, grad

def save_data_to_excel(save_data_path, y_vdd, y_temp, y_rot_speed, y_grad):
    print("Saving data to: ", save_data_path)
    pass

def plot_update(device):
    vdd, temp, rot_speed, grad = ble_read_data(device)
    print(vdd, temp, rot_speed, grad)

def handler(sig_receieved, frame):
    adapter.stop()
    save_data_to_excel(save_data_path, y_vdd, y_temp, y_rot_speed, y_grad)
    print('Goodbye!')
    exit(0)


def main():
    try:
        device = adapter.connect('B0:91:22:0C:61:84')
    except:
        raise Exception("Could not connect to device...\n")
    
    print("Connected to device {}".format(device))

    while(True):
        plot_update(device)
        time.sleep(1)


if __name__ == "__main__":
    signal(SIGINT, handler)

    save_data_path = ""
    serial_port = "COM3"

    y_rot_speed = [0]
    y_grad = [0]
    y_temp = [0]
    y_vdd = [0]

    try:
        adapter = pygatt.BGAPIBackend(serial_port = serial_port)
        adapter.start()
    except:
        raise Exception("Could not detect BLED112 device at {} port".format(serial_port))
    
    main()