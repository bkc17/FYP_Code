import pygatt
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
from signal import signal, SIGINT
from sys import exit

def plot_update(i, xs, y_rot_speed, y_grad, y_temp, y_vdd, device):

    vdd = float(device.char_read("F000BEF204514000B000000000000000").decode())/1000
    temp = round((1035 - float(device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
    rot_speed = int(device.char_read("F000BEEF04514000B000000000000000"))
    grad = int(device.char_read("F000BEF004514000B000000000000000"))
    y_rot_speed.append(rot_speed)
    y_grad.append(grad)
    y_vdd
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
    print('Goodbye!')
    exit(0)


def main():

    xs = []
    y_rot_speed = []
    y_grad = []
    y_temp = []
    y_vdd = []

    try:
        device = adapter.connect('B0:91:22:0C:61:84')
    except:
        raise Exception("Could not connect to device...\n")
    
    print("Connected to device {}".format(device))

    ani = animation.FuncAnimation(fig, plot_update, fargs=(xs, y_rot_speed, y_grad, y_temp, y_vdd, device), interval=1000)
    plt.show()
    # finally:
    #     adapter.stop()


if __name__ == "__main__":
    signal(SIGINT, handler)

    fig = plt.figure(figsize=(10,4))
    ax_rot = fig.add_subplot(1, 2, 1)
    ax_grad = fig.add_subplot(1, 2, 2)

    serial_port = "COM3"
    try:
        adapter = pygatt.BGAPIBackend(serial_port = serial_port)
        adapter.start()
    except:
        raise Exception("Could not detect BLED112 device at {} port".format(serial_port))
    
    main()