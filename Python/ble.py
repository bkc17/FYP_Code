import pygatt
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt

def plot_update(i, xs, ys, device):

    vdd = float(device.char_read("F000BEF204514000B000000000000000").decode())/1000
    temp = round((1035 - float(device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
    rot_speed = int(device.char_read("F000BEEF04514000B000000000000000"))
    grad = int(device.char_read("F000BEF004514000B000000000000000"))
    ys.append(temp)
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f')[:-5])
    xs = xs[-20:]
    ys = ys[-20:]
    ax.clear()
    ax.plot(xs, ys)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.ylabel('Rotation Speed (rads/sec)')

def main():
    adapter = pygatt.BGAPIBackend()

    try:
        adapter.start()
        device = adapter.connect('B0:91:22:0C:61:84')
        ani = animation.FuncAnimation(fig, plot_update, fargs=(xs, ys, device), interval=1000)
        plt.show()
        # while(1):
        #     vdd = float(device.char_read("F000BEF204514000B000000000000000").decode())/1000
        #     temp = round((1035 - float(device.char_read("F000BEF104514000B000000000000000").decode()))/5.5,2)
        #     rot_speed = int(device.char_read("F000BEEF04514000B000000000000000"))
        #     grad = int(device.char_read("F000BEF004514000B000000000000000"))
        #     time.sleep(1)
    finally:
        adapter.stop()


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    main()