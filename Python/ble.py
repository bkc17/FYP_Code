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

def save_data_to_excel():
    print("Saving data to: ", save_data_path)
    pass

def plot_update(i, xs, device):
    vdd, temp, rot_speed, grad = ble_read_data(device)

    y_vdd.append(vdd)
    y_temp.append(temp)
    y_rot_speed.append(rot_speed)
    y_grad.append(grad)
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f')[:-5])

    xs = xs[-10:]
    y_rot_speed_display = y_rot_speed[-10:]
    y_grad_display = y_grad[-10:]

    ax_rot.clear()
    ax_rot.plot(xs, y_rot_speed_display)
    ax_rot.tick_params(labelrotation=45)
    ax_rot.set_title('Rotation Speed (rads/sec)')

    ax_grad.clear()
    ax_grad.plot(xs, y_grad_display)
    ax_grad.tick_params(labelrotation=45)
    ax_grad.set_title('Gradient (rads/ $s^2$)')

    

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

    xs = []
    ani = animation.FuncAnimation(fig, plot_update, fargs=(xs, device), interval = 1000)
    plt.show()

if __name__ == "__main__":
    signal(SIGINT, handler)

    save_data_path = ""
    serial_port = "COM3"

    y_rot_speed = []
    y_grad = []
    y_temp = []
    y_vdd = []

    fig = plt.figure(figsize=(10,5))
    ax_rot = fig.add_subplot(1, 2, 1)
    ax_grad = fig.add_subplot(1, 2, 2)

    try:
        adapter = pygatt.BGAPIBackend(serial_port = serial_port)
        adapter.start()
    except:
        raise Exception("Could not detect BLED112 device at {} port".format(serial_port))
    
    main()